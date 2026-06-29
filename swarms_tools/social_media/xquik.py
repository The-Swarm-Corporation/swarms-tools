"""
Xquik API client for X data workflows.
"""

import os
from typing import Any, Dict, Optional

import httpx


class XquikToolError(Exception):
    """Raised when an Xquik API request fails."""


class XquikTool:
    """
    Small read client for Xquik X data endpoints.

    The client requires an Xquik API key. Pass it directly or set
    XQUIK_API_KEY in the environment.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://xquik.com/api/v1",
        timeout: float = 30.0,
        client: Optional[httpx.Client] = None,
    ) -> None:
        self.api_key = api_key or os.getenv("XQUIK_API_KEY")
        if not self.api_key:
            raise ValueError(
                "XQUIK_API_KEY environment variable is not set"
            )

        self.base_url = base_url.rstrip("/")
        self.client = client or httpx.Client(timeout=timeout)
        self._owns_client = client is None

    def _get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        response = self.client.get(
            f"{self.base_url}{path}",
            headers={
                "accept": "application/json",
                "x-api-key": self.api_key,
            },
            params={
                key: value
                for key, value in (params or {}).items()
                if value is not None
            },
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            raise XquikToolError(
                "Xquik request failed with status "
                f"{response.status_code}"
            ) from error
        return response.json()

    def search_tweets(
        self,
        q: str,
        limit: int = 20,
        query_type: str = "Latest",
        cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Search X posts with X search operators.
        """
        return self._get(
            "/x/tweets/search",
            {
                "q": q,
                "limit": limit,
                "queryType": query_type,
                "cursor": cursor,
            },
        )

    def get_tweet(self, tweet_id: str) -> Dict[str, Any]:
        """
        Fetch one post by its X post ID.
        """
        return self._get(f"/x/tweets/{tweet_id}")

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Fetch one X user by handle or numeric user ID.
        """
        return self._get(f"/x/users/{user_id}")

    def get_user_tweets(
        self,
        user_id: str,
        cursor: Optional[str] = None,
        include_replies: bool = False,
        include_parent_tweet: bool = False,
    ) -> Dict[str, Any]:
        """
        Fetch recent posts for one X user.
        """
        return self._get(
            f"/x/users/{user_id}/tweets",
            {
                "cursor": cursor,
                "includeReplies": str(include_replies).lower(),
                "includeParentTweet": str(
                    include_parent_tweet
                ).lower(),
            },
        )

    def close(self) -> None:
        """
        Close the owned HTTP client.
        """
        if self._owns_client:
            self.client.close()

    def __enter__(self) -> "XquikTool":
        return self

    def __exit__(
        self,
        exc_type: Any,
        exc_value: Any,
        traceback: Any,
    ) -> None:
        self.close()
