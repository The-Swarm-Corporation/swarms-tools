# Swarms Tools

[![Join our Discord](https://img.shields.io/badge/Discord-Join%20our%20server-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/agora-999382051935506503) [![Subscribe on YouTube](https://img.shields.io/badge/YouTube-Subscribe-red?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@kyegomez3242) [![Connect on LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kye-g-38759a207/) [![Follow on X.com](https://img.shields.io/badge/X.com-Follow-1DA1F2?style=for-the-badge&logo=x&logoColor=white)](https://x.com/kyegomezb)

## Overview

**Swarms Tools** is an enterprise-grade Python package designed for seamless integration of cutting-edge APIs into multi-agent orchestration systems. Built for organizations requiring robust, scalable, and maintainable automation solutions, this toolkit provides standardized interfaces for financial data, social media integration, IoT connectivity, and more.

## Key Features

| Feature                                      | Description                                                                                                    |
|-----------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| **Unified API Integration**                   | Production-ready Python functions for enterprise applications                                                  |
| **Enterprise-Grade Architecture**             | Comprehensive type hints, structured outputs, and enterprise documentation standards                           |
| **Multi-Agent System Compatibility**          | Optimized for seamless integration into Swarms' distributed agent orchestration platforms                      |
| **Extensible Framework**                      | Standardized schema for rapid tool development and deployment                                                  |
| **Enterprise Security**                       | Secure API key management and compliance-ready implementation patterns                                         |
| **Bleeding Edge Performance**                 | Utilizes high-performance libraries such as `httpx` for async HTTP and `orjson` for ultra-fast serialization   |

## Installation

```bash
pip3 install -U swarms-tools
```

## Project Structure

```plaintext
swarms-tools/
├── swarms_tools/
│   ├── finance/
│   │   ├── htx_tool.py
│   │   ├── eodh_api.py
│   │   ├── coingecko_tool.py
│   │   └── defillama_mcp_tools.py
│   ├── social_media/
│   │   └── telegram_tool.py
│   ├── utilities/
│   │   └── logging.py
├── tests/
│   ├── test_financial_data.py
│   └── test_social_media.py
└── README.md
```

## Enterprise Use Cases

### Financial Data Management

Our comprehensive financial tools enable organizations to streamline operations and gain actionable insights:

| Tool Name | Function | Description |
|-----------|----------|-------------|
| `fetch_stock_news` | `fetch_stock_news` | Retrieves real-time stock news and market updates |
| `fetch_htx_data` | `fetch_htx_data` | Accesses financial data from HTX trading platform |
| `yahoo_finance_api` | `yahoo_finance_api` | Comprehensive stock data including pricing and trend analysis |
| `coin_gecko_coin_api` | `coin_gecko_coin_api` | Cryptocurrency market data and pricing information |
| `helius_api_tool` | `helius_api_tool` | Blockchain account, transaction, and token data via Helius API |
| `okx_api_tool` | `okx_api_tool` | Detailed cryptocurrency data from OKX exchange |
| `defillama_mcp_tools` | `get_protocol_tvl, get_chain_tvl, get_token_prices, make_request` | DeFi ecosystem data including protocol TVL and token pricing |

#### Financial Data Retrieval Examples

**Historical Data Analysis**
```python
from swarms_tools import fetch_htx_data

# Retrieve historical trading data for analysis
response = fetch_htx_data("swarms")
print(response)
```

**Market News Intelligence**
```python
from swarms_tools import fetch_stock_news

# Access latest market news for strategic decision-making
news = fetch_stock_news("AAPL")
print(news)
```

**Cryptocurrency Market Analysis**
```python
from swarms_tools import coin_gecko_coin_api

# Real-time cryptocurrency market data
crypto_data = coin_gecko_coin_api("bitcoin")
print(crypto_data)
```

**DeFi Protocol Analytics**
```python
from swarms_tools import get_protocol_tvl

# Protocol TVL data for investment analysis
protocol_tvl = await get_protocol_tvl("uniswap-v3")
print(protocol_tvl)
```

### Social Media Automation

Streamline corporate communication and engagement strategies:

**Telegram Integration Example**
```python
from swarms_tools import telegram_dm_or_tag_api

def send_corporate_alert(response: str):
    telegram_dm_or_tag_api(response)

# Automated corporate communication
send_corporate_alert("Critical business update from Swarms Corporation.")
```

## Dex Screener Integration

Enterprise-grade tool for accessing decentralized exchange data across multiple blockchain networks:

```python
from swarms_tools.finance.dex_screener import (
    fetch_latest_token_boosts,
    fetch_dex_screener_profiles,
)

# Retrieve token boost data
fetch_dex_screener_profiles()
fetch_latest_token_boosts()
```

## Tool Orchestration Framework

The tool chainer enables sequential or parallel execution of multiple tools for complex workflow automation:

```python
from loguru import logger
from swarms_tools.structs import tool_chainer

if __name__ == "__main__":
    logger.add("tool_chainer.log", rotation="500 MB", level="INFO")

    # Define enterprise tools
    def data_analysis_tool():
        return "Data Analysis Complete"

    def reporting_tool():
        return "Report Generated"

    tools = [data_analysis_tool, reporting_tool]

    # Parallel execution for performance optimization
    parallel_results = tool_chainer(tools, parallel=True)
    print("Parallel Results:", parallel_results)

    # Sequential execution for dependency management
    sequential_results = tool_chainer(tools, parallel=False)
    print("Sequential Results:", sequential_results)
```

## Social Media Management

### Twitter API Integration

Comprehensive Twitter automation for enterprise social media management:

```python
import os
from time import time
from swarm_models import OpenAIChat
from swarms import Agent
from dotenv import load_dotenv
from swarms_tools.social_media.twitter_tool import TwitterTool

load_dotenv()

# Initialize enterprise AI model
model_name = "gpt-4o"
model = OpenAIChat(
    model_name=model_name,
    max_tokens=3000,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

# Configure Twitter integration
options = {
    "id": "29998836",
    "name": "mcsswarm",
    "description": "Enterprise Twitter automation platform",
    "credentials": {
        "apiKey": os.getenv("TWITTER_API_KEY"),
        "apiSecretKey": os.getenv("TWITTER_API_SECRET_KEY"),
        "accessToken": os.getenv("TWITTER_ACCESS_TOKEN"),
        "accessTokenSecret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    },
}

twitter_plugin = TwitterTool(options)
post_tweet = twitter_plugin.get_function("post_tweet")

# Automated content generation and posting
def generate_corporate_content():
    content_prompt = "Generate professional corporate content for social media engagement"
    tweet_text = model.run(content_prompt)
    
    try:
        post_tweet(tweet_text)
        print(f"Content posted successfully: {tweet_text}")
    except Exception as e:
        print(f"Error posting content: {e}")
```

## Enterprise Development Standards

Every tool in **Swarms Tools** adheres to enterprise-grade development standards:

### Development Schema

1. **Modular Architecture**: Encapsulate API logic into reusable, maintainable functions
2. **Type Safety**: Comprehensive Python type hints for input validation and code clarity
3. **Documentation**: Detailed docstrings with parameter specifications and usage examples
4. **Output Standardization**: Consistent return formats for seamless system integration
5. **Security Compliance**: Secure API key management using environment variables

#### Schema Template

```python
def enterprise_data_function(parameter: str, date_range: str) -> str:
    """
    Enterprise-grade data retrieval function.

    Args:
        parameter (str): Business parameter for data retrieval
        date_range (str): Timeframe specification (e.g., '1d', '1m', '1y')

    Returns:
        str: Structured data response for enterprise systems
    """
    pass
```

## Documentation and Support

Comprehensive enterprise documentation is available at [docs.swarms.world](https://docs.swarms.world), providing detailed API references, implementation guides, and best practices for enterprise deployment.

## Community and Support

Join our enterprise community for technical support, platform updates, and exclusive access to advanced agent engineering insights:

| Platform | Description | Link |
|----------|-------------|------|
| Discord | Live technical support and community | [Join Discord](https://discord.gg/EamjgSaEQf) |
| Twitter | Platform updates and announcements | [@swarms_corp](https://twitter.com/swarms_corp) |
| YouTube | Technical tutorials and demonstrations | [Swarms Channel](https://www.youtube.com/channel/UC9yXyitkbU_WSy7bd_41SqQ) |
| Documentation | Official technical documentation | [docs.swarms.world](https://docs.swarms.world) |
| Blog | Technical articles and platform insights | [Medium](https://medium.com/@kyeg) |
| LinkedIn | Professional network and corporate updates | [The Swarm Corporation](https://www.linkedin.com/company/the-swarm-corporation) |
| Events | Enterprise community events and workshops | [Sign up here](https://lu.ma/5p2jnc2v) |
| Onboarding | Enterprise onboarding with platform experts | [Book Session](https://cal.com/swarms/swarms-onboarding-session) |

## Contributing

We welcome enterprise contributions and partnerships. To contribute:

1. **Fork the Repository**: Begin by forking the main repository
2. **Create Feature Branch**: Use descriptive naming: `feature/enterprise-tool-name`
3. **Implement Standards**: Follow enterprise development guidelines
4. **Submit Pull Request**: Open pull request for technical review

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for complete terms and conditions.

---

**"The future belongs to those who dare to automate it."**  
**— The Swarms Corporation**

