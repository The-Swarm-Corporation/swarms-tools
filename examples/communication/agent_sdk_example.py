"""
Agent SDK Example

This example demonstrates how to use the Agent SDK for blockchain-based agent communication.
The Agent SDK enables agents to communicate securely on blockchain networks with cryptographic proofs.

Requirements:
- AGENT_PROXY_ADDRESS environment variable (optional, has default)
- NETWORK_RPC environment variable (optional, has default)
- AGENT_CONTRACT environment variable (optional, has default)
- AGENT_SIGNERS environment variable (optional, has default list)
- CONVERTER_ADDRESS environment variable (optional, has default)
- AGENT_PRIVATE_KEY environment variable (for registration/verification)
- Install required dependencies: ai-agent, loguru, python-dotenv

Usage:
    python agent_sdk_example.py
"""

import os
from dotenv import load_dotenv
from loguru import logger
from swarms_tools.communication.agent_sdk import AgentSDKManager

# Load environment variables
load_dotenv()


def main():
    """
    Main function demonstrating Agent SDK usage.
    """
    logger.info("Starting Agent SDK example...")
    
    try:
        # Initialize Agent SDK Manager (uses defaults if env vars not set)
        logger.info("Initializing Agent SDK Manager...")
        agent_manager = AgentSDKManager()
        
        # Display current configuration
        logger.info("Current Agent SDK Configuration:")
        logger.info(f"  Proxy Address: {agent_manager.AGENT_PROXY_ADDRESS}")
        logger.info(f"  Network RPC: {agent_manager.NETWORK_RPC}")
        logger.info(f"  Agent Contract: {agent_manager.AGENT_CONTRACT}")
        logger.info(f"  Default Signers: {len(agent_manager.default_signers)} signers")
        
        # Example 1: Create agent settings
        logger.info("Example 1: Creating agent settings")
        settings = agent_manager.create_agent_settings(
            threshold=2,
            converter_address=os.getenv("CONVERTER_ADDRESS")
        )
        logger.info(f"Agent settings created successfully")
        logger.info(f"  Signers: {len(settings.signers)}")
        logger.info(f"  Threshold: {settings.threshold}")
        logger.info(f"  Converter Address: {settings.converter_address}")
        logger.info(f"  Agent Name: {settings.agent_header.source_agent_name}")
        
        # Example 2: Create agent payload
        logger.info("Example 2: Creating agent payload")
        payload = agent_manager.create_agent_payload(
            data="Hello from agent communication example",
            data_hash="0x1234567890abcdef1234567890abcdef12345678",
            zk_proof="0xproof1234567890abcdef",
            merkle_proof="0xmerkle4567890abcdef",
            signature_proof="0xsig7890abcdef123456"
        )
        logger.info(f"Agent payload created successfully")
        logger.info(f"  Data: {payload.data}")
        logger.info(f"  Data Hash: {payload.data_hash}")
        logger.info(f"  ZK Proof: {payload.proofs.zk_proof}")
        logger.info(f"  Merkle Proof: {payload.proofs.merkle_proof}")
        logger.info(f"  Signature Proof: {payload.proofs.signature_proof}")
        
        # Example 3: Register new agent (requires private key)
        private_key = os.getenv("AGENT_PRIVATE_KEY")
        if private_key:
            logger.info("Example 3: Registering new agent")
            try:
                result = agent_manager.register_new_agent(
                    private_key=private_key,
                    settings=settings
                )
                logger.info(f"Agent registration result: {result}")
            except Exception as e:
                logger.warning(f"Agent registration failed (this is expected in demo): {e}")
        else:
            logger.warning("AGENT_PRIVATE_KEY not found, skipping agent registration example")
            logger.info("To test agent registration, set AGENT_PRIVATE_KEY in your .env file")
        
        # Example 4: Verify agent data (requires private key)
        if private_key:
            logger.info("Example 4: Verifying agent data")
            try:
                verify_result = agent_manager.verify_agent_data(
                    private_key=private_key,
                    settings_digest="0xsettings_digest1234567890abcdef",
                    payload=payload
                )
                logger.info(f"Agent verification result: {verify_result}")
            except Exception as e:
                logger.warning(f"Agent verification failed (this is expected in demo): {e}")
        
        # Example 5: Different agent configurations
        logger.info("Example 5: Different agent configurations")
        
        # High security configuration
        high_security_settings = agent_manager.create_agent_settings(
            threshold=5,  # Higher threshold for more security
            converter_address=os.getenv("CONVERTER_ADDRESS")
        )
        logger.info(f"High security settings created with threshold: {high_security_settings.threshold}")
        
        # Custom signers configuration
        custom_signers = [
            "0x1234567890abcdef1234567890abcdef12345678",
            "0xabcdef1234567890abcdef1234567890abcdef12",
            "0x567890abcdef1234567890abcdef1234567890ab"
        ]
        custom_settings = agent_manager.create_agent_settings(
            signers=custom_signers,
            threshold=2
        )
        logger.info(f"Custom settings created with {len(custom_settings.signers)} custom signers")
        
        logger.info("Agent SDK examples completed successfully!")
        logger.info("Note: Registration and verification require valid blockchain credentials")
        
    except Exception as e:
        logger.error(f"Error with Agent SDK: {e}")
        logger.info("Make sure all required dependencies are installed")
        logger.info("The Agent SDK uses default values for most configuration")


if __name__ == "__main__":
    main()
