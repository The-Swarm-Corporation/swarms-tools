"""
Epic FHIR Integration Example

This example demonstrates how to use the Epic FHIR integration tools to interact with
Epic healthcare systems for patient data management, observations, and medical records.

Requirements:
- FHIR_BASE_URL environment variable (optional, has default)
- OAUTH_TOKEN_URL environment variable (optional, has default)
- EPIC_CLIENT_ID environment variable (optional, has default)
- EPIC_CLIENT_SECRET environment variable (optional, has default)
- EPIC_SCOPE environment variable (optional, has default)
- Install required dependencies: httpx, loguru, python-dotenv, backoff, pydantic, mcp

Usage:
    python epic_integration_example.py
"""

import os
import asyncio
from dotenv import load_dotenv
from loguru import logger
from swarms_tools.healthcare.epic_integration import (
    search_patients,
    get_patient_by_id,
    get_patient_observations,
    add_patient_resource,
    add_observation_resource,
    get_encounters_for_patient,
    get_medications_for_patient,
    get_appointments,
    get_conditions
)

# Load environment variables
load_dotenv()


async def main():
    """
    Main function demonstrating Epic FHIR integration usage.
    """
    logger.info("Starting Epic FHIR Integration example...")
    
    # Display current configuration (uses defaults if env vars not set)
    logger.info("Current Epic FHIR Configuration:")
    logger.info(f"  FHIR Base URL: {os.getenv('FHIR_BASE_URL', 'https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4')}")
    logger.info(f"  OAuth Token URL: {os.getenv('OAUTH_TOKEN_URL', 'https://epic.oauth.com/token')}")
    logger.info(f"  Client ID: {os.getenv('EPIC_CLIENT_ID', 'Not set')}")
    logger.info(f"  Client Secret: {'Set' if os.getenv('EPIC_CLIENT_SECRET') else 'Not set'}")
    logger.info(f"  Scope: {os.getenv('EPIC_SCOPE', 'patient/*.read')}")
    
    try:
        # Example 1: Search for patients
        logger.info("Example 1: Searching for patients")
        patient_name = "John Doe"
        try:
            patients = await search_patients(patient_name)
            logger.info(f"Search results for '{patient_name}': {len(patients.get('entry', []))} patients found")
            if patients.get('entry'):
                for patient in patients['entry'][:2]:  # Show first 2 patients
                    resource = patient.get('resource', {})
                    logger.info(f"  - Patient ID: {resource.get('id', 'N/A')}")
                    names = resource.get('name', [])
                    if names:
                        name = names[0]
                        given = ' '.join(name.get('given', []))
                        family = name.get('family', '')
                        logger.info(f"    Name: {given} {family}")
        except Exception as e:
            logger.warning(f"Could not search for patients: {e}")
        
        # Example 2: Get patient by ID (using a sample ID)
        logger.info("Example 2: Getting patient by ID")
        sample_patient_id = "12345"  # Replace with actual patient ID
        try:
            patient = await get_patient_by_id(sample_patient_id)
            logger.info(f"Patient details retrieved successfully")
            logger.info(f"  Patient ID: {patient.get('id', 'N/A')}")
            logger.info(f"  Resource Type: {patient.get('resourceType', 'N/A')}")
            names = patient.get('name', [])
            if names:
                name = names[0]
                given = ' '.join(name.get('given', []))
                family = name.get('family', '')
                logger.info(f"  Name: {given} {family}")
        except Exception as e:
            logger.warning(f"Could not fetch patient {sample_patient_id}: {e}")
        
        # Example 3: Get patient observations
        logger.info("Example 3: Getting patient observations")
        try:
            observations = await get_patient_observations(sample_patient_id)
            logger.info(f"Found {len(observations.get('entry', []))} observations for patient")
            if observations.get('entry'):
                for obs in observations['entry'][:2]:  # Show first 2 observations
                    resource = obs.get('resource', {})
                    logger.info(f"  - Observation ID: {resource.get('id', 'N/A')}")
                    logger.info(f"    Status: {resource.get('status', 'N/A')}")
                    code = resource.get('code', {})
                    if code:
                        codings = code.get('coding', [])
                        if codings:
                            logger.info(f"    Code: {codings[0].get('display', 'N/A')}")
        except Exception as e:
            logger.warning(f"Could not fetch observations: {e}")
        
        # Example 4: Get patient encounters
        logger.info("Example 4: Getting patient encounters")
        try:
            encounters = await get_encounters_for_patient(sample_patient_id)
            logger.info(f"Found {len(encounters.get('entry', []))} encounters for patient")
            if encounters.get('entry'):
                for enc in encounters['entry'][:2]:  # Show first 2 encounters
                    resource = enc.get('resource', {})
                    logger.info(f"  - Encounter ID: {resource.get('id', 'N/A')}")
                    logger.info(f"    Status: {resource.get('status', 'N/A')}")
                    logger.info(f"    Class: {resource.get('class', {}).get('code', 'N/A')}")
        except Exception as e:
            logger.warning(f"Could not fetch encounters: {e}")
        
        # Example 5: Get patient medications
        logger.info("Example 5: Getting patient medications")
        try:
            medications = await get_medications_for_patient(sample_patient_id)
            logger.info(f"Found {len(medications.get('entry', []))} medications for patient")
            if medications.get('entry'):
                for med in medications['entry'][:2]:  # Show first 2 medications
                    resource = med.get('resource', {})
                    logger.info(f"  - Medication Request ID: {resource.get('id', 'N/A')}")
                    logger.info(f"    Status: {resource.get('status', 'N/A')}")
                    logger.info(f"    Intent: {resource.get('intent', 'N/A')}")
        except Exception as e:
            logger.warning(f"Could not fetch medications: {e}")
        
        # Example 6: Get patient appointments
        logger.info("Example 6: Getting patient appointments")
        try:
            appointments = await get_appointments(sample_patient_id)
            logger.info(f"Found {len(appointments.get('entry', []))} appointments for patient")
            if appointments.get('entry'):
                for apt in appointments['entry'][:2]:  # Show first 2 appointments
                    resource = apt.get('resource', {})
                    logger.info(f"  - Appointment ID: {resource.get('id', 'N/A')}")
                    logger.info(f"    Status: {resource.get('status', 'N/A')}")
                    logger.info(f"    Start: {resource.get('start', 'N/A')}")
        except Exception as e:
            logger.warning(f"Could not fetch appointments: {e}")
        
        # Example 7: Get patient conditions
        logger.info("Example 7: Getting patient conditions")
        try:
            conditions = await get_conditions(sample_patient_id)
            logger.info(f"Found {len(conditions.get('entry', []))} conditions for patient")
            if conditions.get('entry'):
                for cond in conditions['entry'][:2]:  # Show first 2 conditions
                    resource = cond.get('resource', {})
                    logger.info(f"  - Condition ID: {resource.get('id', 'N/A')}")
                    logger.info(f"    Clinical Status: {resource.get('clinicalStatus', {}).get('coding', [{}])[0].get('code', 'N/A')}")
                    code = resource.get('code', {})
                    if code:
                        codings = code.get('coding', [])
                        if codings:
                            logger.info(f"    Condition: {codings[0].get('display', 'N/A')}")
        except Exception as e:
            logger.warning(f"Could not fetch conditions: {e}")
        
        # Example 8: Add new patient resource (commented out to avoid creating test data)
        logger.info("Example 8: Adding new patient resource (commented out)")
        logger.info("To test patient creation, uncomment the following code:")
        logger.info("# sample_patient_data = {")
        logger.info("#     'resourceType': 'Patient',")
        logger.info("#     'name': [{'family': 'Smith', 'given': ['Jane']}],")
        logger.info("#     'gender': 'female',")
        logger.info("#     'birthDate': '1990-01-01'")
        logger.info("# }")
        logger.info("# new_patient = await add_patient_resource(sample_patient_data)")
        logger.info("# logger.info(f'Created new patient: {new_patient.get('id', 'N/A')}')")
        
        # Example 9: Add new observation resource (commented out to avoid creating test data)
        logger.info("Example 9: Adding new observation resource (commented out)")
        logger.info("To test observation creation, uncomment the following code:")
        logger.info("# sample_observation_data = {")
        logger.info("#     'resourceType': 'Observation',")
        logger.info("#     'status': 'final',")
        logger.info("#     'code': {'coding': [{'system': 'http://loinc.org', 'code': '33747-0', 'display': 'Blood pressure'}]},")
        logger.info("#     'subject': {'reference': f'Patient/{sample_patient_id}'},")
        logger.info("#     'valueQuantity': {'value': 120, 'unit': 'mmHg'}")
        logger.info("# }")
        logger.info("# new_observation = await add_observation_resource(sample_observation_data)")
        logger.info("# logger.info(f'Created new observation: {new_observation.get('id', 'N/A')}')")
        
        logger.info("Epic FHIR Integration examples completed successfully!")
        logger.info("Note: This example uses default Epic configuration values")
        logger.info("For production use, set proper Epic environment variables")
        
    except Exception as e:
        logger.error(f"Error with Epic FHIR integration: {e}")
        logger.info("Make sure all required dependencies are installed")
        logger.info("The Epic integration uses default values for most configuration")


if __name__ == "__main__":
    asyncio.run(main())
