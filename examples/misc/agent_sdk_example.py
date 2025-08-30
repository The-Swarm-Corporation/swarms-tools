from swarms_tools.communication.agent_sdk import AgentSDKManager


def main():
    # Initialize the AgentSDKManager
    agent_manager = AgentSDKManager()

    # Example private key (replace with your actual private key)
    private_key = "YOUR_PRIVATE_KEY"

    # Create custom agent settings (optional)
    settings = agent_manager.create_agent_settings(
        threshold=3,  # Custom threshold
        converter_address="0xCustomConverterAddress",  # Custom converter address
    )

    # Register a new agent
    registration_result = agent_manager.register_new_agent(
        private_key=private_key, settings=settings
    )
    print("Agent Registration Result:", registration_result)

    # Create a sample payload
    sample_payload = agent_manager.create_agent_payload(
        data="0xSampleData",
        data_hash="0xSampleDataHash",
        signature_proof="0xSampleSignatureProof",
    )

    # Verify the agent data
    verification_result = agent_manager.verify_agent_data(
        private_key=private_key,
        settings_digest="0xSampleSettingsDigest",
        payload=sample_payload,
    )
    print("Verification Result:", verification_result)


if __name__ == "__main__":
    main()
