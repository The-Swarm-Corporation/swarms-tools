import os
from dotenv import load_dotenv
from swarms_tools.communication.agent_sdk import AgentSDKManager

load_dotenv()

# Test AgentSDKManager initialization
agent_manager = AgentSDKManager()
assert agent_manager is not None

# Test that required methods exist
assert hasattr(agent_manager, 'create_agent_settings')
assert hasattr(agent_manager, 'create_agent_payload')
assert hasattr(agent_manager, 'register_new_agent')
assert hasattr(agent_manager, 'verify_agent_data')

# Test that methods are callable
assert callable(agent_manager.create_agent_settings)
assert callable(agent_manager.create_agent_payload)
assert callable(agent_manager.register_new_agent)
assert callable(agent_manager.verify_agent_data)

# Test agent settings creation
settings = agent_manager.create_agent_settings(
    threshold=2,
    converter_address=os.getenv("CONVERTER_ADDRESS")
)
assert settings is not None
assert hasattr(settings, 'signers')
assert hasattr(settings, 'threshold')
assert hasattr(settings, 'agent_header')
assert len(settings.signers) > 0
assert settings.threshold == 2

# Test agent payload creation
payload = agent_manager.create_agent_payload(
    data="Hello from agent communication example",
    data_hash="0x1234567890abcdef1234567890abcdef12345678",
    zk_proof="0xproof1234567890abcdef",
    merkle_proof="0xmerkle4567890abcdef",
    signature_proof="0xsig7890abcdef123456"
)
assert payload is not None
assert hasattr(payload, 'data')
assert hasattr(payload, 'data_hash')
assert hasattr(payload, 'proofs')
assert payload.data == "Hello from agent communication example"
assert payload.data_hash == "0x1234567890abcdef1234567890abcdef12345678"

# Test that proofs are properly structured
assert hasattr(payload.proofs, 'zk_proof')
assert hasattr(payload.proofs, 'merkle_proof')
assert hasattr(payload.proofs, 'signature_proof')
assert payload.proofs.zk_proof == "0xproof1234567890abcdef"
assert payload.proofs.merkle_proof == "0xmerkle4567890abcdef"
assert payload.proofs.signature_proof == "0xsig7890abcdef123456"
