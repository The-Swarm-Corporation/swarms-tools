"""Unit tests for the Jupiter Protocol API tools using custom test framework."""

import orjson
import asyncio
import aiohttp
from datetime import datetime
from unittest.mock import patch, MagicMock
from swarms_tools.finance.jupiter_tools import (
    jupiter_fetch_token_by_mint_address,
    jupiter_fetch_token_by_mint_address_async,
    jupiter_fetch_tradable_tokens,
    jupiter_fetch_tradable_tokens_async,
    jupiter_get_token_prices,
    jupiter_get_token_prices_async,
)

# Test Results Storage
test_results = {
    "timestamp": "",
    "total_tests": 0,
    "passed": 0,
    "failed": 0,
    "results": [],
}

# Sample test data
SAMPLE_TOKEN = {
    "address": "So11111111111111111111111111111111111111112",
    "chainId": 101,
    "decimals": 9,
    "name": "Wrapped SOL",
    "symbol": "SOL",
    "logoURI": (
        "https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/So11111111111111111111111111111111111111112/logo.png"
    ),
}

SAMPLE_PRICES = {
    "data": {
        "So11111111111111111111111111111111111111112": {
            "id": "So11111111111111111111111111111111111111112",
            "mintSymbol": "SOL",
            "vsToken": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            "vsTokenSymbol": "USDC",
            "price": 100.50,
        }
    }
}


def run_test(func):
    """Decorator to run tests and record results."""

    def wrapper(*args, **kwargs):
        test_results["total_tests"] += 1
        test_name = func.__name__
        try:
            func(*args, **kwargs)
            test_results["passed"] += 1
            test_results["results"].append(
                {
                    "test_name": test_name,
                    "status": "passed",
                    "error": None,
                }
            )
            print(f"✅ {test_name} passed")
        except Exception as e:
            test_results["failed"] += 1
            test_results["results"].append(
                {
                    "test_name": test_name,
                    "status": "failed",
                    "error": str(e),
                }
            )
            print(f"❌ {test_name} failed: {str(e)}")

    return wrapper


def run_async_test(func):
    """Decorator to run async tests and record results."""

    def wrapper(*args, **kwargs):
        test_results["total_tests"] += 1
        test_name = func.__name__
        try:
            asyncio.run(func(*args, **kwargs))
            test_results["passed"] += 1
            test_results["results"].append(
                {
                    "test_name": test_name,
                    "status": "passed",
                    "error": None,
                }
            )
            print(f"✅ {test_name} passed")
        except Exception as e:
            test_results["failed"] += 1
            test_results["results"].append(
                {
                    "test_name": test_name,
                    "status": "failed",
                    "error": str(e),
                }
            )
            print(f"❌ {test_name} failed: {str(e)}")

    return wrapper


async def create_mock_session():
    """Create a mock aiohttp session for testing."""
    mock = MagicMock()
    mock.__aenter__.return_value = mock
    mock.raise_for_status = MagicMock()
    return mock


@run_async_test
async def test_fetch_token_by_mint_address_async():
    """Test fetching token information by mint address asynchronously."""
    mock_session = await create_mock_session()
    mint_address = "So11111111111111111111111111111111111111112"

    with patch(
        "swarms_tools.finance.jupiter_tools.get_aiohttp_session"
    ) as mock_get_session:
        mock_get_session.return_value = mock_session
        mock_session.json.return_value = SAMPLE_TOKEN

        result = await jupiter_fetch_token_by_mint_address_async(
            mint_address
        )

        assert result == SAMPLE_TOKEN
        assert result["symbol"] == "SOL"
        assert result["address"] == mint_address


@run_test
def test_fetch_token_by_mint_address():
    """Test the synchronous wrapper for fetching token information."""
    mint_address = "So11111111111111111111111111111111111111112"

    with patch(
        "swarms_tools.finance.jupiter_tools.jupiter_fetch_token_by_mint_address_async"
    ) as mock_async:
        mock_async.return_value = SAMPLE_TOKEN

        result = jupiter_fetch_token_by_mint_address(mint_address)

        assert result == SAMPLE_TOKEN


@run_async_test
async def test_get_token_prices_async():
    """Test getting token prices asynchronously with different parameter combinations."""
    mock_session = await create_mock_session()
    token_ids = ["So11111111111111111111111111111111111111112"]

    with patch(
        "swarms_tools.finance.jupiter_tools.get_aiohttp_session"
    ) as mock_get_session:
        mock_get_session.return_value = mock_session
        mock_session.json.return_value = SAMPLE_PRICES

        # Test with single token ID
        result = await jupiter_get_token_prices_async(token_ids[0])
        assert result == SAMPLE_PRICES

        # Test with list of token IDs
        result = await jupiter_get_token_prices_async(token_ids)
        assert result == SAMPLE_PRICES

        # Test with vs_token parameter
        result = await jupiter_get_token_prices_async(
            token_ids, vs_token="USDC"
        )
        assert result == SAMPLE_PRICES


@run_async_test
async def test_get_token_prices_invalid_params():
    """Test getting token prices with invalid parameter combinations."""
    token_ids = ["So11111111111111111111111111111111111111112"]
    try:
        await jupiter_get_token_prices_async(
            token_ids, vs_token="USDC", show_extra_info=False
        )
        raise AssertionError("Expected ValueError was not raised")
    except ValueError:
        pass


@run_test
def test_get_token_prices():
    """Test the synchronous wrapper for getting token prices."""
    token_ids = ["So11111111111111111111111111111111111111112"]

    with patch(
        "swarms_tools.finance.jupiter_tools.jupiter_get_token_prices_async"
    ) as mock_async:
        mock_async.return_value = SAMPLE_PRICES
        result = jupiter_get_token_prices(token_ids)
        assert result == SAMPLE_PRICES


@run_async_test
async def test_fetch_tradable_tokens_async():
    """Test fetching tradable tokens asynchronously."""
    mock_session = await create_mock_session()
    sample_tradable_tokens = [SAMPLE_TOKEN]

    with patch(
        "swarms_tools.finance.jupiter_tools.get_aiohttp_session"
    ) as mock_get_session:
        mock_get_session.return_value = mock_session
        mock_session.json.return_value = sample_tradable_tokens
        result = await jupiter_fetch_tradable_tokens_async()
        assert result == sample_tradable_tokens


@run_test
def test_fetch_tradable_tokens():
    """Test the synchronous wrapper for fetching tradable tokens."""
    sample_tradable_tokens = [SAMPLE_TOKEN]

    with patch(
        "swarms_tools.finance.jupiter_tools.jupiter_fetch_tradable_tokens_async"
    ) as mock_async:
        mock_async.return_value = sample_tradable_tokens
        result = jupiter_fetch_tradable_tokens()
        assert result == sample_tradable_tokens


@run_async_test
async def test_api_error_handling():
    """Test error handling for API requests."""
    mock_session = await create_mock_session()
    mint_address = "So11111111111111111111111111111111111111112"

    with patch(
        "swarms_tools.finance.jupiter_tools.get_aiohttp_session"
    ) as mock_get_session:
        mock_get_session.return_value = mock_session
        mock_session.raise_for_status.side_effect = (
            aiohttp.ClientError()
        )

        try:
            await jupiter_fetch_token_by_mint_address_async(
                mint_address
            )
            raise AssertionError(
                "Expected ClientError was not raised"
            )
        except aiohttp.ClientError:
            pass


def run_all_tests():
    """Run all tests and generate JSON report."""
    test_results["timestamp"] = datetime.now().isoformat()

    # Run all test functions
    test_fetch_token_by_mint_address_async()
    test_fetch_token_by_mint_address()
    test_get_token_prices_async()
    test_get_token_prices_invalid_params()
    test_get_token_prices()
    test_fetch_tradable_tokens_async()
    test_fetch_tradable_tokens()
    test_api_error_handling()

    # Generate report
    report_path = "jupiter_test_report.json"
    with open(report_path, "w") as f:
        orjson.dump(test_results, f, option=orjson.OPT_INDENT_2)

    print("\nTest Summary:")
    print(f"Total Tests: {test_results['total_tests']}")
    print(f"Passed: {test_results['passed']}")
    print(f"Failed: {test_results['failed']}")
    print(f"\nDetailed report saved to: {report_path}")


if __name__ == "__main__":
    run_all_tests()
