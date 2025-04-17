import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from ai_agent.agent import AgentSDK
from ai_agent.entities import (
    AgentSettings,
    AgentHeader,
    MessageType,
    Priority,
    AgentMessagePayload,
    Proofs,
    AgentMetadata,
)
from ai_agent.utils import generate_uuid_v4
import time


class AgentSDKManager:
    def __init__(
        self,
        signers: Optional[list] = None,
        threshold: int = 2,
        converter_address: Optional[str] = None,
    ):
        # Load environment variables
        load_dotenv()

        # Default network settings
        self.AGENT_PROXY_ADDRESS = os.getenv("AGENT_PROXY_ADDRESS")
        self.NETWORK_RPC = os.getenv("NETWORK_RPC")
        self.AGENT_CONTRACT = os.getenv("AGENT_CONTRACT")

        # Initialize AgentSDK
        self.agent = AgentSDK(
            endpoint_uri=self.NETWORK_RPC,
            proxy_address=self.AGENT_PROXY_ADDRESS,
        )

        # Default signers from environment or fallback to predefined list
        self.default_signers = signers

    def create_agent_settings(
        self,
        signers: Optional[list] = None,
        threshold: int = 2,
        converter_address: Optional[str] = None,
    ) -> AgentSettings:
        """Create agent settings with dynamic header"""
        if not converter_address:
            converter_address = os.getenv("CONVERTER_ADDRESS")

        return AgentSettings(
            signers=signers or self.default_signers,
            threshold=threshold,
            converter_address=converter_address,
            agent_header=AgentHeader(
                version="1.0",
                message_id=generate_uuid_v4(),
                source_agent_id=generate_uuid_v4(),
                source_agent_name="APRO Pull Mode Agent",
                target_agent_id=generate_uuid_v4(),
                timestamp=int(time.time()),
                message_type=MessageType.Event,
                priority=Priority.Low,
                ttl=60 * 60,
            ),
        )

    def register_new_agent(
        self,
        private_key: str,
        settings: Optional[AgentSettings] = None,
        transmitter: str = "",
        nonce: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Register a new agent with the provided settings"""
        if not settings:
            settings = self.create_agent_settings()

        self.agent.add_account(private_key)
        result = self.agent.create_and_register_agent(
            transmitter=transmitter, nonce=nonce, settings=settings
        )
        return result

    def verify_agent_data(
        self,
        private_key: str,
        settings_digest: str,
        payload: AgentMessagePayload,
        transmitter: str = "",
        nonce: Optional[int] = None,
        agent_contract: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Verify agent data integrity"""
        if not agent_contract:
            agent_contract = self.AGENT_CONTRACT

        self.agent.add_account(private_key)
        result = self.agent.verify(
            transmitter=transmitter,
            nonce=nonce,
            agent_contract=agent_contract,
            settings_digest=settings_digest,
            payload=payload,
        )
        return result

    @staticmethod
    def create_agent_payload(
        data: str,
        data_hash: str,
        zk_proof: str = "0x",
        merkle_proof: str = "0x",
        signature_proof: str = "0x",
        content_type: str = "0x",
        encoding: str = "0x",
        compression: str = "0x",
    ) -> AgentMessagePayload:
        """Create an agent message payload with the provided data and proofs"""
        return AgentMessagePayload(
            data=data,
            data_hash=data_hash,
            proofs=Proofs(
                zk_proof=zk_proof,
                merkle_proof=merkle_proof,
                signature_proof=signature_proof,
            ),
            meta_data=AgentMetadata(
                content_type=content_type,
                encoding=encoding,
                compression=compression,
            ),
        )


def create_agent_settings(
    signers: Optional[list] = None,
    threshold: int = 2,
    converter_address: Optional[str] = None,
) -> Dict[str, Any]:
    """Create agent settings with specified signers and threshold

    Args:
        signers: Optional list of signer addresses
        threshold: Number of required signers (default: 2)
        converter_address: Optional address of converter contract

    Returns:
        Dict containing the created agent settings
    """
    manager = AgentSDKManager()
    settings = manager.create_agent_settings(
        signers, threshold, converter_address
    )
    print(settings)
    return settings


def register_new_agent(
    private_key: str,
    transmitter: str = "",
    nonce: Optional[int] = None,
) -> Dict[str, Any]:
    """Register a new agent with the provided private key

    Args:
        private_key: Private key of the agent
        transmitter: Address of the transmitter contract
        nonce: Optional nonce value

    Returns:
        Dict containing registration result
    """
    manager = AgentSDKManager()
    result = manager.register_new_agent(
        private_key, transmitter, nonce
    )
    print(result)
    return result


def verify_agent_data(
    private_key: str,
    settings_digest: str,
    payload: AgentMessagePayload,
    transmitter: str = "",
    nonce: Optional[int] = None,
    agent_contract: Optional[str] = None,
) -> Dict[str, Any]:
    """Verify agent data with provided parameters

    Args:
        private_key: Private key of the agent
        settings_digest: Digest of agent settings
        payload: Agent message payload object
        transmitter: Address of transmitter contract
        nonce: Optional nonce value
        agent_contract: Optional agent contract address

    Returns:
        Dict containing verification result
    """
    manager = AgentSDKManager()
    result = manager.verify_agent_data(
        private_key,
        settings_digest,
        payload,
        transmitter,
        nonce,
        agent_contract,
    )
    print(result)
    return result


def create_agent_payload(
    data: str,
    data_hash: str,
    zk_proof: str = "0x",
    merkle_proof: str = "0x",
    signature_proof: str = "0x",
    content_type: str = "0x",
    encoding: str = "0x",
    compression: str = "0x",
) -> AgentMessagePayload:
    """Create an agent message payload with the provided data and proofs

    Args:
        data: Data string
        data_hash: Hash of the data
        zk_proof: Zero-knowledge proof (default: "0x")
        merkle_proof: Merkle tree proof (default: "0x")
        signature_proof: Signature proof (default: "0x")
        content_type: Content type (default: "0x")
        encoding: Encoding type (default: "0x")
        compression: Compression type (default: "0x")

    Returns:
        AgentMessagePayload object containing the payload data
    """
    manager = AgentSDKManager()
    payload = manager.create_agent_payload(
        data,
        data_hash,
        zk_proof,
        merkle_proof,
        signature_proof,
        content_type,
        encoding,
        compression,
    )
    print(payload)
    return payload
