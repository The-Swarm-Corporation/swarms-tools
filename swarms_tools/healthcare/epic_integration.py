import os
from functools import lru_cache
from typing import Any, Dict, List, Optional

import backoff
import httpx
from mcp.server.fastmcp import FastMCP
from loguru import logger
from pydantic import BaseModel, Field, HttpUrl, validator

# Initialize MCP
mcp = FastMCP("epic-mcp")


class EpicAPIError(Exception):
    """Base exception for Epic API errors"""

    pass


class EpicAuthenticationError(EpicAPIError):
    """Raised when authentication fails"""

    pass


class EpicConfigurationError(EpicAPIError):
    """Raised when configuration is invalid"""

    pass


class EpicConfig(BaseModel):
    """Configuration model for Epic integration"""

    fhir_base_url: Optional[HttpUrl] = Field(
        default="https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4"
    )
    oauth_token_url: Optional[HttpUrl] = Field(
        default="https://epic.oauth.com/token"
    )
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    scope: Optional[str] = Field(default="patient/*.read")

    @validator("client_id", "client_secret")
    def validate_credentials(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v.strip()) == 0:
            raise EpicConfigurationError(
                "Credentials cannot be empty"
            )
        return v


class OAuthToken(BaseModel):
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None


class Patient(BaseModel):
    id: Optional[str] = None
    name: Optional[List[Dict[str, Any]]] = None
    birthDate: Optional[str] = None
    gender: Optional[str] = None
    active: Optional[bool] = None


class Observation(BaseModel):
    id: Optional[str] = None
    status: Optional[str] = None
    code: Optional[Dict[str, Any]] = None
    subject: Optional[Dict[str, Any]] = None
    effectiveDateTime: Optional[str] = None
    valueQuantity: Optional[Dict[str, Any]] = None


# Load configuration
try:
    config = EpicConfig(
        fhir_base_url=os.getenv("FHIR_BASE_URL"),
        oauth_token_url=os.getenv("OAUTH_TOKEN_URL"),
        client_id=os.getenv("EPIC_CLIENT_ID"),
        client_secret=os.getenv("EPIC_CLIENT_SECRET"),
        scope=os.getenv("EPIC_SCOPE"),
    )
except Exception as e:
    raise EpicConfigurationError(
        f"Failed to load configuration: {str(e)}"
    )


@backoff.on_exception(
    backoff.expo, (httpx.HTTPError, EpicAPIError), max_tries=3
)
@lru_cache(maxsize=1)
async def get_access_token() -> str:
    """
    Obtain or cache an OAuth access token.

    Returns:
        str: The access token

    Raises:
        EpicAuthenticationError: If authentication fails
        EpicAPIError: For other API-related errors
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                str(config.oauth_token_url),
                data={
                    "grant_type": "client_credentials",
                    "client_id": config.client_id,
                    "client_secret": config.client_secret,
                    "scope": config.scope,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            token = OAuthToken(**response.json())
            logger.debug("Successfully obtained new access token")
            return token.access_token
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise EpicAuthenticationError("Authentication failed")
        raise EpicAPIError(f"Failed to obtain access token: {str(e)}")
    except Exception as e:
        raise EpicAPIError(
            f"Unexpected error obtaining access token: {str(e)}"
        )


@backoff.on_exception(
    backoff.expo, (httpx.HTTPError, EpicAPIError), max_tries=3
)
async def fhir_get(
    endpoint: str, params: Optional[dict] = None
) -> Dict[str, Any]:
    """
    Helper to perform GET on FHIR API with retries and error handling.

    Args:
        endpoint: API endpoint to call
        params: Optional query parameters

    Returns:
        Dict containing the API response

    Raises:
        EpicAPIError: If the API call fails
    """
    try:
        token = await get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/fhir+json",
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{config.fhir_base_url}/{endpoint}",
                headers=headers,
                params=params,
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise EpicAPIError(f"FHIR API error: {str(e)}")
    except Exception as e:
        raise EpicAPIError(f"Unexpected error in FHIR GET: {str(e)}")


@backoff.on_exception(
    backoff.expo, (httpx.HTTPError, EpicAPIError), max_tries=3
)
async def fhir_post(
    endpoint: str, data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Helper to POST a resource to the FHIR API with retries and error handling.

    Args:
        endpoint: API endpoint to call
        data: Data to POST

    Returns:
        Dict containing the API response

    Raises:
        EpicAPIError: If the API call fails
    """
    try:
        token = await get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/fhir+json",
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{config.fhir_base_url}/{endpoint}",
                headers=headers,
                json=data,
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise EpicAPIError(f"FHIR API error: {str(e)}")
    except Exception as e:
        raise EpicAPIError(f"Unexpected error in FHIR POST: {str(e)}")


#########################
# MCP TOOLS START HERE ##
#########################


@mcp.tool(
    name="search_patients",
    description="Search for patients in the Epic system by their name",
)
@logger.catch
async def search_patients(name: str) -> dict:
    """
    Search for patients by name.

    Args:
        name: Patient name to search for

    Returns:
        Dict containing matching patients
    """
    logger.info(f"Searching for patients with name: {name}")
    return await fhir_get("Patient", {"name": name})


@mcp.tool(
    name="get_patient_by_id",
    description="Retrieve detailed information about a specific patient using their ID",
)
@logger.catch
async def get_patient_by_id(patient_id: str) -> dict:
    """
    Get a single patient by ID.

    Args:
        patient_id: The patient's ID

    Returns:
        Dict containing patient information
    """
    logger.info(f"Fetching patient with ID: {patient_id}")
    return await fhir_get(f"Patient/{patient_id}")


@mcp.tool(
    name="get_patient_observations",
    description="Retrieve all medical observations and measurements for a specific patient",
)
@logger.catch
async def get_patient_observations(patient_id: str) -> dict:
    """
    Fetch all Observations for a Patient.

    Args:
        patient_id: The patient's ID

    Returns:
        Dict containing patient observations
    """
    logger.info(f"Fetching observations for patient ID: {patient_id}")
    return await fhir_get(
        "Observation", {"subject": f"Patient/{patient_id}"}
    )


@mcp.tool(
    name="add_patient_resource",
    description="Create a new patient record in the Epic system with provided patient information",
)
@logger.catch
async def add_patient_resource(patient_data: dict) -> dict:
    """
    Create a new Patient resource in EPIC.

    Args:
        patient_data: Patient information to add

    Returns:
        Dict containing the created patient resource
    """
    logger.info("Creating new patient resource")
    try:
        # Validate patient data
        Patient(**patient_data)
        return await fhir_post("Patient", patient_data)
    except Exception as e:
        logger.error(f"Invalid patient data: {str(e)}")
        raise EpicAPIError(f"Invalid patient data: {str(e)}")


@mcp.tool(
    name="add_observation_resource",
    description="Add a new medical observation or measurement for a patient",
)
@logger.catch
async def add_observation_resource(observation_data: dict) -> dict:
    """
    Add a new Observation resource.

    Args:
        observation_data: Observation information to add

    Returns:
        Dict containing the created observation resource
    """
    logger.info("Creating new observation resource")
    try:
        # Validate observation data
        Observation(**observation_data)
        return await fhir_post("Observation", observation_data)
    except Exception as e:
        logger.error(f"Invalid observation data: {str(e)}")
        raise EpicAPIError(f"Invalid observation data: {str(e)}")


@mcp.tool(
    name="get_encounters_for_patient",
    description="Retrieve all clinical encounters and visits for a specific patient",
)
@logger.catch
async def get_encounters_for_patient(patient_id: str) -> dict:
    """
    Retrieve encounters for a patient.

    Args:
        patient_id: The patient's ID

    Returns:
        Dict containing patient encounters
    """
    logger.info(f"Fetching encounters for patient ID: {patient_id}")
    return await fhir_get(
        "Encounter", {"subject": f"Patient/{patient_id}"}
    )


@mcp.tool(
    name="get_medications_for_patient",
    description="Retrieve all medication requests and prescriptions for a specific patient",
)
@logger.catch
async def get_medications_for_patient(patient_id: str) -> dict:
    """
    Retrieve medication requests for a patient.

    Args:
        patient_id: The patient's ID

    Returns:
        Dict containing patient medications
    """
    logger.info(f"Fetching medications for patient ID: {patient_id}")
    return await fhir_get(
        "MedicationRequest", {"subject": f"Patient/{patient_id}"}
    )


@mcp.tool(
    name="get_appointments",
    description="Retrieve all scheduled appointments for a specific patient",
)
@logger.catch
async def get_appointments(patient_id: str) -> dict:
    """
    Fetch appointments for a patient.

    Args:
        patient_id: The patient's ID

    Returns:
        Dict containing patient appointments
    """
    logger.info(f"Fetching appointments for patient ID: {patient_id}")
    return await fhir_get(
        "Appointment", {"actor": f"Patient/{patient_id}"}
    )


@mcp.tool(
    name="get_conditions",
    description="Retrieve all medical conditions and diagnoses for a specific patient",
)
@logger.catch
async def get_conditions(patient_id: str) -> dict:
    """
    Fetch all conditions related to a patient.

    Args:
        patient_id: The patient's ID

    Returns:
        Dict containing patient conditions
    """
    logger.info(f"Fetching conditions for patient ID: {patient_id}")
    return await fhir_get(
        "Condition", {"subject": f"Patient/{patient_id}"}
    )


def start_epic_mcp():
    mcp.run(transport="sse")


# if __name__ == "__main__":
#     start_epic_mcp()
