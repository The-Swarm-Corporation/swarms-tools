# Swarms Tools

[![Join our Discord](https://img.shields.io/badge/Discord-Join%20our%20server-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/agora-999382051935506503) [![Subscribe on YouTube](https://img.shields.io/badge/YouTube-Subscribe-red?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@kyegomez3242) [![Connect on LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kye-g-38759a207/) [![Follow on X.com](https://img.shields.io/badge/X.com-Follow-1DA1F2?style=for-the-badge&logo=x&logoColor=white)](https://x.com/kyegomezb)


Welcome to **Swarms Tools**, the ultimate package for integrating **cutting-edge APIs** into Python functions with seamless multi-agent system compatibility. Designed for enterprises at the forefront of innovation, **Swarms Tools** is your key to simplifying complexity and unlocking operational excellence.

---

## 🚀 Features

- **Unified API Integration**: Ready-to-use Python functions for financial data, social media, IoT, and more.
- **Enterprise-Grade Design**: Comprehensive type hints, structured outputs, and robust documentation.
- **Agent-Ready Framework**: Optimized for seamless integration into Swarms' multi-agent orchestration systems.
- **Expandable Architecture**: Easily extend functionality with a standardized schema for new tools.

---

## 🔧 Installation

```bash
pip3 install -U swarms-tools
```

---

## 📂 Directory Structure

```plaintext
swarms-tools/
├── swarms_tools/
│   ├── finance/
│   │   ├── htx_tool.py
│   │   ├── eodh_api.py
│   │   └── coingecko_tool.py
│   │   └── defillama_mcp_tools.py
│   ├── social_media/
│   │   ├── telegram_tool.py
│   ├── utilities/
│   │   └── logging.py
├── tests/
│   ├── test_financial_data.py
│   └── test_social_media.py
└── README.md
```

---

## 💼 Use Cases



## Finance

Explore our diverse range of financial tools, designed to streamline your operations. If you need a tool not listed, feel free to submit an issue or accelerate integration by contributing a pull request with your tool of choice.

| **Tool Name**             | **Function**             | **Description**                                                                 |
|---------------------------|--------------------------|---------------------------------------------------------------------------------|
| `fetch_stock_news`        | `fetch_stock_news`       | Fetches the latest stock news and updates.                                     |
| `fetch_htx_data`          | `fetch_htx_data`         | Retrieves financial data from the HTX platform.                                |
| `yahoo_finance_api`       | `yahoo_finance_api`      | Fetches comprehensive stock data from Yahoo Finance, including prices and trends. |
| `coin_gecko_coin_api`     | `coin_gecko_coin_api`    | Fetches cryptocurrency data from CoinGecko, including market and price information. |
| `helius_api_tool`         | `helius_api_tool`        | Retrieves blockchain account, transaction, or token data using the Helius API. |
| `okx_api_tool`            | `okx_api_tool`           | Fetches detailed cryptocurrency data for coins from the OKX exchange.         |
| `defillama_mcp_tools`            | `get_protocol_tvl,get_chain_tvl,get_token_prices,make_request`           | Provides access to DeFi Llama API for retrieving protocol TVL, chain TVL, and token price data across DeFi ecosystems. |


### Financial Data Retrieval
Enable precise and actionable financial insights:

#### Example 1: Fetch Historical Data
```python
from swarms_tools import fetch_htx_data

# Fetch historical trading data for "Swarms Corporation"
response = fetch_htx_data("swarms")
print(response)
```

#### Example 2: Stock News Analysis
```python
from swarms_tools import fetch_stock_news

# Retrieve latest stock news for Apple
news = fetch_stock_news("AAPL")
print(news)
```

#### Example 3: Cryptocurrency Metrics
```python
from swarms_tools import coin_gecko_coin_api

# Fetch live data for Bitcoin
crypto_data = coin_gecko_coin_api("bitcoin")
print(crypto_data)
```


#### Example 4: Get Defi protocol TVL
``` python
from swarms_tools import get_protocol_tvl

# Fetching protocol TVL for uniswap-v3
protocol_tvl = await get_protocol_tvl("uniswap-v3")
print(protocol_tvl)
```

### Social Media Automation
Streamline communication and engagement:

#### Example: Telegram Bot Messaging
```python
from swarms_tools import telegram_dm_or_tag_api

def send_alert(response: str):
    telegram_dm_or_tag_api(response)

# Send a message to a user or group
send_alert("Mission-critical update from Swarms.")
```

---

## Dex Screener

This is a tool that allows you to fetch data from the Dex Screener API. It supports multiple chains and multiple tokens.

```python
from swarms_tools.finance.dex_screener import (
    fetch_latest_token_boosts,
    fetch_dex_screener_profiles,
)


fetch_dex_screener_profiles()
fetch_latest_token_boosts()

```

---


## Structs
The tool chainer enables the execution of multiple tools in a sequence, allowing for the aggregation of their results in either a parallel or sequential manner.

```python
# Example usage
from loguru import logger

from swarms_tools.structs import tool_chainer


if __name__ == "__main__":
    logger.add("tool_chainer.log", rotation="500 MB", level="INFO")

    # Example tools
    def tool1():
        return "Tool1 Result"

    def tool2():
        return "Tool2 Result"

    # def tool3():
    #     raise ValueError("Simulated error in Tool3")

    tools = [tool1, tool2]

    # Parallel execution
    parallel_results = tool_chainer(tools, parallel=True)
    print("Parallel Results:", parallel_results)

    # Sequential execution
    # sequential_results = tool_chainer(tools, parallel=False)
    # print("Sequential Results:", sequential_results)

```
---

## Social Media

- Twitter API Tool

```python
import os
from time import time

from swarm_models import OpenAIChat
from swarms import Agent
from dotenv import load_dotenv

from swarms_tools.social_media.twitter_tool import TwitterTool

load_dotenv()

model_name = "gpt-4o"

model = OpenAIChat(
    model_name=model_name,
    max_tokens=3000,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)


medical_coder = Agent(
    agent_name="Medical Coder",
    system_prompt="""
    You are a highly experienced and certified medical coder with extensive knowledge of ICD-10 coding guidelines, clinical documentation standards, and compliance regulations. Your responsibility is to ensure precise, compliant, and well-documented coding for all clinical cases.

    ### Primary Responsibilities:
    1. **Review Clinical Documentation**: Analyze all available clinical records, including specialist inputs, physician notes, lab results, imaging reports, and discharge summaries.
    2. **Assign Accurate ICD-10 Codes**: Identify and assign appropriate codes for primary diagnoses, secondary conditions, symptoms, and complications.
    3. **Ensure Coding Compliance**: Follow the latest ICD-10-CM/PCS coding guidelines, payer-specific requirements, and organizational policies.
    4. **Document Code Justification**: Provide clear, evidence-based rationale for each assigned code.

    ### Detailed Coding Process:
    - **Review Specialist Inputs**: Examine all relevant documentation to capture the full scope of the patient's condition and care provided.
    - **Identify Diagnoses**: Determine the primary and secondary diagnoses, as well as any symptoms or complications, based on the documentation.
    - **Assign ICD-10 Codes**: Select the most accurate and specific ICD-10 codes for each identified diagnosis or condition.
    - **Document Supporting Evidence**: Record the documentation source (e.g., lab report, imaging, or physician note) for each code to justify its assignment.
    - **Address Queries**: Note and flag any inconsistencies, missing information, or areas requiring clarification from providers.

    ### Output Requirements:
    Your response must be clear, structured, and compliant with professional standards. Use the following format:

    1. **Primary Diagnosis Codes**:
        - **ICD-10 Code**: [e.g., E11.9]
        - **Description**: [e.g., Type 2 diabetes mellitus without complications]
        - **Supporting Documentation**: [e.g., Physician's note dated MM/DD/YYYY]
        
    2. **Secondary Diagnosis Codes**:
        - **ICD-10 Code**: [Code]
        - **Description**: [Description]
        - **Order of Clinical Significance**: [Rank or priority]

    3. **Symptom Codes**:
        - **ICD-10 Code**: [Code]
        - **Description**: [Description]

    4. **Complication Codes**:
        - **ICD-10 Code**: [Code]
        - **Description**: [Description]
        - **Relevant Documentation**: [Source of information]

    5. **Coding Notes**:
        - Observations, clarifications, or any potential issues requiring provider input.

    ### Additional Guidelines:
    - Always prioritize specificity and compliance when assigning codes.
    - For ambiguous cases, provide a brief note with reasoning and flag for clarification.
    - Ensure the output format is clean, consistent, and ready for professional use.
    """,
    llm=model,
    max_loops=1,
    dynamic_temperature_enabled=True,
)


# Define your options with the necessary credentials
options = {
    "id": "29998836",
    "name": "mcsswarm",
    "description": "An example Twitter Plugin for testing.",
    "credentials": {
        "apiKey": os.getenv("TWITTER_API_KEY"),
        "apiSecretKey": os.getenv("TWITTER_API_SECRET_KEY"),
        "accessToken": os.getenv("TWITTER_ACCESS_TOKEN"),
        "accessTokenSecret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    },
}

# Initialize the TwitterTool with your options
twitter_plugin = TwitterTool(options)

# # Post a tweet
# post_tweet_fn = twitter_plugin.get_function('post_tweet')
# post_tweet_fn("Hello world!")


# Assuming `twitter_plugin` and `medical_coder` are already initialized
post_tweet = twitter_plugin.get_function("post_tweet")

# Set to track posted tweets and avoid duplicates
posted_tweets = set()


def post_unique_tweet():
    """
    Generate and post a unique tweet. Skip duplicates.
    """
    tweet_prompt = (
        "Share an intriguing, lesser-known fact about a medical disease, and include an innovative, fun, or surprising way to manage or cure it! "
        "Make the response playful, engaging, and inspiring—something that makes people smile while learning. No markdown, just plain text!"
    )

    # Generate a new tweet text
    tweet_text = medical_coder.run(tweet_prompt)

    # Check for duplicates
    if tweet_text in posted_tweets:
        print("Duplicate tweet detected. Skipping...")
        return

    # Post the tweet
    try:
        post_tweet(tweet_text)
        print(f"Posted tweet: {tweet_text}")
        # Add the tweet to the set of posted tweets
        posted_tweets.add(tweet_text)
    except Exception as e:
        print(f"Error posting tweet: {e}")


# Loop to post tweets every 10 seconds
def start_tweet_loop(interval=10):
    """
    Continuously post tweets every `interval` seconds.

    Args:
        interval (int): Time in seconds between tweets.
    """
    print("Starting tweet loop...")
    while True:
        post_unique_tweet()
        time.sleep(interval)


# Start the loop
start_tweet_loop(10)


```

## 🧩 Standardized Schema

Every tool in **Swarms Tools** adheres to a strict schema for maintainability and interoperability:

### Schema Template

1. **Functionality**:
   - Encapsulate API logic into a modular, reusable function.

2. **Typing**:
   - Leverage Python type hints for input validation and clarity.

   Example:
   ```python
   def fetch_data(symbol: str, date_range: str) -> str:
       """
       Fetch financial data for a given symbol and date range.

       Args:
           symbol (str): Ticker symbol of the asset.
           date_range (str): Timeframe for the data (e.g., '1d', '1m', '1y').

       Returns:
           dict: A dictionary containing financial metrics.
       """
       pass
   ```

3. **Documentation**:
   - Include detailed docstrings with parameter explanations and usage examples.

4. **Output Standardization**:
   - Ensure consistent outputs (e.g., strings) for easy downstream agent integration.

5. **API-Key Management**:
    - All API keys must be fetched with `os.getenv("YOUR_KEY")`


---

## 📖 Documentation

Comprehensive documentation is available to guide developers and enterprises. Visit our [official docs](https://docs.swarms.world) for detailed API references, usage examples, and best practices.

---

## 🛠 Contributing

We welcome contributions from the global developer community. To contribute:

1. **Fork the Repository**: Start by forking the repository.
2. **Create a Feature Branch**: Use a descriptive branch name: `feature/add-new-tool`.
3. **Commit Your Changes**: Write meaningful commit messages.
4. **Submit a Pull Request**: Open a pull request for review.

---

## 🛡️ License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🌠 Join the Future

Explore the limitless possibilities of agent-based systems. Together, we can build a smarter, faster, and more interconnected world.

**Visit us:** [Swarms Corporation](https://swarms.ai)  
**Follow us:** [Twitter](https://twitter.com/swarms_corp)

---

**"The future belongs to those who dare to automate it."**  
**— The Swarms Corporation**

