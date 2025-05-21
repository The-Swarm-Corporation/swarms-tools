from loguru import logger
import time
import os
from dotenv import load_dotenv

from swarms_tools.agents.attps import ATTPsVerify
from attps.verify.entities import  (
    AgentSettings,
    AgentMessagePayload,
    AgentHeader,
    MessageType,
    AgentMetadata,
    Priority,
    Proofs,
    AgentRegisterResults,
    AgentMessageVerifiedResults,
)


AGENT_PROXY_ADDRESS = "0x5E787A4131Cf9fC902C99235df5C8314C816DA11"
NETWORK_RPC = "https://data-seed-prebsc-2-s1.bnbchain.org:8545"

AGENT_PROXY_TYPE_VERSION = "AI Agent Proxy 1.0.0"
AGENT_SETTINGS = AgentSettings(
    signers = [
        "0x4b1056f504f32c678227b5Ae812936249c40AfBF",
        "0xB973476e0cF88a3693014b99f230CEB5A01ac686",
        "0x6cF0803D049a4e8DC01da726A5a212BCB9FAC1a1",
        "0x9D46daa26342e9E9e586A6AdCEDaD667f985567B",
        "0x33AF673aBcE193E20Ee94D6fBEb30fEf0cA7015b",
        "0x868D2dE4a0378450BC62A7596463b30Dc4e3897E",
        "0xD4E157c36E7299bB40800e4aE7909DDcA8097f67",
        "0xA3866A07ABEf3fD0643BD7e1c32600520F465ca8",
        "0x62f642Ae0Ed7F12Bc40F2a9Bf82ccD0a3F3b7531"
    ], # Signer list corresponding to the Agent's signed data
    threshold = 2, # Verification threshold, minimum number of correct signatures from signers
    converter_address="0x24c36e9996eb84138Ed7cAa483B4c59FF7640E5C", # Converter contract address for intermediate data processing between signed data and final signed data
    agent_header = AgentHeader(
        version =  "1.0", # agent version
        message_id="d4d0813f-ceb7-4ce1-8988-12899b26c4b6", # Agent‘s Message ID, Used for target agent uniqueness verification
        source_agent_id = "da70f6b3-e580-470f-b88b-caa5369e7778", # Source Agent ID, globally unique in the system
        source_agent_name = "APRO Pull Mode Agent", # Source agent name
        target_agent_id = "d4d0813f-ceb7-4ce1-8988-12899b26c4b6", # Target Agent ID
        timestamp =  int(time.time()), # Agent registration time
        message_type = MessageType.Event, # Agent data transmission type, currently only supports Event
        priority = Priority.Low,
        ttl = 60 * 60
    )
)

AGENT_CONTRACT = "0x77b83A1Ac194b1Faf266Dc66C77D2eA6A6B7f26d" # Verification contract corresponding to the agent
AGENT_SETTING_DIGEST = "0x0100dbf9fbd3d502b0f285c44f741212fc97db83e31ca91627c2e8b43b00f2ae" # Agent's configuration information identifier, returned in the blockchain event during registration or modification
AGENT_PAYLOAD = AgentMessagePayload(
    data = "0x0006e706cf7ab41fa599311eb3de68be869198ce62aef1cd079475ca50e5b3f60000000000000000000000000000000000000000000000000000000002b1bf0e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000022000000000000000000000000000000000000000000000000000000000000002a0000101000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001200003665949c883f9e0f6f002eac32e00bd59dfe6c34e92a91c37d6a8322d6489000000000000000000000000000000000000000000000000000000006762677d000000000000000000000000000000000000000000000000000000006762677d000000000000000000000000000000000000000000000000000003128629ec0800000000000000000000000000000000000000000000000004db732547630000000000000000000000000000000000000000000000000000000000006763b8fd0000000000000000000000000000000000000000000015f0f60671beb95cc0000000000000000000000000000000000000000000000015f083baa654a7b900000000000000000000000000000000000000000000000015f103ec7cb057ea80000000000000000000000000000000000000000000000000000000000000000003b64f7e72208147bb898e8b215d0997967bef0219263726c76995d8a19107d6ba5306a176474f9ccdb1bc5841f97e0592013e404e15b0de0839b81d0efb26179f222e0191269a8560ebd9096707d225bc606d61466b85d8568d7620a3b59a73e800000000000000000000000000000000000000000000000000000000000000037cae0f05c1bf8353eb5db27635f02b40a534d4192099de445764891198231c597a303cd15f302dafbb1263eb6e8e19cbacea985c66c6fed3231fd84a84ebe0276f69f481fe7808c339a04ceb905bb49980846c8ceb89a27b1c09713cb356f773",
    data_hash = "0x53d9f133f1265bd4391fcdf89b63424cbcfd316c8448f76cc515647267ac0a8e", # Hash of the corresponding data
    proofs = Proofs (
        zk_proof = "0x",
        merkle_proof = "0x",
        signature_proof = "0x000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000e000000000000000000000000000000000000000000000000000000000000001600000000000000000000000000000000000000000000000000000000000000003b64f7e72208147bb898e8b215d0997967bef0219263726c76995d8a19107d6ba5306a176474f9ccdb1bc5841f97e0592013e404e15b0de0839b81d0efb26179f222e0191269a8560ebd9096707d225bc606d61466b85d8568d7620a3b59a73e800000000000000000000000000000000000000000000000000000000000000037cae0f05c1bf8353eb5db27635f02b40a534d4192099de445764891198231c597a303cd15f302dafbb1263eb6e8e19cbacea985c66c6fed3231fd84a84ebe0276f69f481fe7808c339a04ceb905bb49980846c8ceb89a27b1c09713cb356f7730000000000000000000000000000000000000000000000000000000000000003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001",
    ),
    meta_data = AgentMetadata (
        content_type = "0x",
        encoding= "0x",
        compression= "0x"
    )
)

if __name__ == "__main__":
    # Set up logging
    logger.add(
        "attps.log", rotation="500 MB", level="INFO"
    )

    load_dotenv()
    transmitter_private_key = os.getenv("TRANSMITTER_PRIVATE_KEY")

    # Example usage
    agent = ATTPsVerify(
        endpoint_uri=NETWORK_RPC,
        proxy_address=AGENT_PROXY_ADDRESS,
        transmitter_private_keys=[transmitter_private_key],
    )

    print(agent.transmitters())

    result = agent.register_agent(transmitter= agent.transmitters()[0], settings=AGENT_SETTINGS)
    print("register agent result", result)

    result = agent.verify(
        transmitter=agent.transmitters()[0],
        agent_contract=AGENT_CONTRACT,
        settings_digest=AGENT_SETTING_DIGEST,
        payload=AGENT_PAYLOAD
    )
    print("verify agent message result, hash:", result.hash)
