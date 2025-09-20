import os
from dotenv import load_dotenv
from swarms_tools.communication.agent_sdk import AgentSDKManager

load_dotenv()

agent_manager = AgentSDKManager()

# Create agent settings with custom configuration
settings = agent_manager.create_agent_settings(
    threshold=2,
    converter_address=os.getenv("CONVERTER_ADDRESS")
)

# Create agent payload with cryptographic proofs
payload = agent_manager.create_agent_payload(
    data="Hello from agent communication example",
    data_hash="0x1234567890abcdef1234567890abcdef12345678",
    zk_proof="0xproof1234567890abcdef",
    merkle_proof="0xmerkle4567890abcdef",
    signature_proof="0xsig7890abcdef123456"
)

print(f"Agent settings created: {len(settings.signers)} signers, threshold {settings.threshold}")
print(f"Agent payload created with data: {payload.data}")
print(f"ZK Proof: {payload.proofs.zk_proof}")

# Try to register agent if private key is available
private_key = os.getenv("AGENT_PRIVATE_KEY")
if private_key:
    try:
        result = agent_manager.register_new_agent(private_key=private_key, settings=settings)
        print(f"Agent registration result: {result}")
    except Exception as e:
        print(f"Agent registration failed (expected in demo): {e}")
else:
    print("AGENT_PRIVATE_KEY not found, skipping registration")
