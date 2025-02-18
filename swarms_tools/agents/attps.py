import attps
from attps.verify.agent import (
    AgentSDK
)
from attps.verify.entities import  (
    AgentSettings,
    AgentMessagePayload,
    AgentRegisterResults,
    AgentMessageVerifiedResults,
)

from loguru import logger

class ATTPsVerify:
    """
    A production-grade client for interacting with APRO ATTPs's API.

    Attributes:
        endpoint_uri (str): Base URL for Jupiter API
        proxy_address(str): Aiohttp session for making requests
        transmitter_private_keys(list[str]): Private key for submitting the transaction.
    """

    def __init__(
            self,
            endpoint_uri: str,
            proxy_address: str,
            transmitter_private_keys: list[str]
    ):
        """Initialize the ATTPs client."""
        self.agent = AgentSDK(endpoint_uri=endpoint_uri, proxy_address=proxy_address)
        for key in transmitter_private_keys:
            self.agent.add_account(private_key=key)

    def transmitters(
        self,
    ) -> list[str]:
        """
        get the transmitters

        Args:


        Returns:
            list[str]: Return the transmitter address list

        Raises:

        """

        return self.agent.accounts()

    def register_agent(
        self,
        transmitter:str,
        settings: AgentSettings
    ) -> AgentRegisterResults:
        """
        Register an agent.

        Args:
            transmitter(str): Address for submitting the transaction.
            settings (AgentSettings): Agent settings

        Returns:
            AgentRegisterResults: Return the corresponding agent address and on-chain hash.

        Raises:
            ValueError: If the transmitter is not valid
        """
        try:
            result = self.agent.create_and_register_agent(
                transmitter=transmitter,
                nonce=None,
                settings=settings
            )
            return result
        except ValueError as e:
            logger.error(
                f"{str(e)}"
            )
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error while register agent: {str(e)}"
            )
            raise

    def verify(
            self,
            transmitter: str,
            agent_contract: str,
            settings_digest: str,
            payload: AgentMessagePayload
    ) -> AgentMessageVerifiedResults:
        """
        verify a message by agent.

        Args:
            transmitter(str): Address for submitting the transaction.
            agent_contract(str): # Verification contract corresponding to the agent
            settings_digest(str): Agent's configuration information identifier, returned in the blockchain event during registration or modification
            payload (AgentMessagePayload): Agent message

        Returns:
            AgentMessageVerifiedResults: Return the corresponding agent message and on-chain hash.

        Raises:
            ValueError: If the transmitter or other address is not valid
        """
        try:
            result = self.agent.verify(
                transmitter=self.agent.accounts()[0],
                nonce=None,
                agent_contract=agent_contract,
                settings_digest=settings_digest,
                payload=payload
            )
            return result
        except ValueError as e:
            logger.error(
                f"{str(e)}"
            )
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error while verify message: {str(e)}"
            )
            raise


