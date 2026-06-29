from importlib import util
from pathlib import Path

import httpx


def load_xquik_tool():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "swarms_tools"
        / "social_media"
        / "xquik.py"
    )
    spec = util.spec_from_file_location("xquik_tool", module_path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.XquikTool


XquikTool = load_xquik_tool()


def test_search_tweets_sends_expected_request():
    requests = []

    def handler(request):
        requests.append(request)
        return httpx.Response(200, json={"tweets": []})

    tool = XquikTool(
        api_key="test-key",
        base_url="https://xquik.test/api/v1",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    result = tool.search_tweets("AI agents", limit=5)

    assert result == {"tweets": []}
    assert len(requests) == 1
    assert requests[0].url.path == "/api/v1/x/tweets/search"
    assert requests[0].url.params["q"] == "AI agents"
    assert requests[0].url.params["limit"] == "5"
    assert requests[0].headers["x-api-key"] == "test-key"


def test_get_user_tweets_uses_user_timeline_route():
    requests = []

    def handler(request):
        requests.append(request)
        return httpx.Response(200, json={"tweets": []})

    tool = XquikTool(
        api_key="test-key",
        base_url="https://xquik.test/api/v1",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    result = tool.get_user_tweets("swarms_corp", include_replies=True)

    assert result == {"tweets": []}
    assert len(requests) == 1
    assert (
        requests[0].url.path
        == "/api/v1/x/users/swarms_corp/tweets"
    )
    assert requests[0].url.params["includeReplies"] == "true"
    assert requests[0].url.params["includeParentTweet"] == "false"
