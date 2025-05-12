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
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Default network settings
        self.AGENT_PROXY_ADDRESS = os.getenv(
            "AGENT_PROXY_ADDRESS",
            "0x07771A3026E60776deC8C1C61106FB9623521394",
        )
        self.NETWORK_RPC = os.getenv(
            "NETWORK_RPC", "https://testnet-rpc.bitlayer.org"
        )
        self.AGENT_CONTRACT = os.getenv(
            "AGENT_CONTRACT",
            "0xA1903361Ee8Ec35acC7c8951b4008dbE8D12C155",
        )

        # Initialize AgentSDK
        self.agent = AgentSDK(
            endpoint_uri=self.NETWORK_RPC,
            proxy_address=self.AGENT_PROXY_ADDRESS,
        )

        # Default signers from environment or fallback to predefined list
        self.default_signers = os.getenv(
            "AGENT_SIGNERS",
            [
                "0x4b1056f504f32c678227b5Ae812936249c40AfBF",
                "0xB973476e0cF88a3693014b99f230CEB5A01ac686",
                "0x6cF0803D049a4e8DC01da726A5a212BCB9FAC1a1",
                "0x9D46daa26342e9E9e586A6AdCEDaD667f985567B",
                "0x33AF673aBcE193E20Ee94D6fBEb30fEf0cA7015b",
                "0x868D2dE4a0378450BC62A7596463b30Dc4e3897E",
                "0xD4E157c36E7299bB40800e4aE7909DDcA8097f67",
                "0xA3866A07ABEf3fD0643BD7e1c32600520F465ca8",
                "0x62f642Ae0Ed7F12Bc40F2a9Bf82ccD0a3F3b7531",
            ],
        )

    def create_agent_settings(
        self,
        signers: Optional[list] = None,
        threshold: int = 2,
        converter_address: Optional[str] = None,
    ) -> AgentSettings:
        """Create agent settings with dynamic header"""
        if not converter_address:
            converter_address = os.getenv(
                "CONVERTER_ADDRESS",
                "0xaB303EF87774D9D259d1098E9aA4dD6c07F69240",
            )

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
