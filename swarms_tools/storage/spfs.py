import os
import io
import uuid
from typing import overload
from types import TracebackType
from urllib.parse import urljoin

import httpx


class SpfsStorageClient:

    def __init__(
        self,
        rpc_url: str = os.getenv(
            "SPFS_RPC_URL",
            "https://sds-gateway-uswest.thestratos.org/spfs/PSu46EiNUYevTVA8doNHiCAFrxU=",
        ),
        timeout: int | None = None,
    ):
        if not rpc_url.endswith("/"):
            rpc_url += "/"

        base_url = urljoin(rpc_url, "api/v0")
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
        )
        self._async_client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
        )

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        self._client.close()

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        await self._async_client.close()

    async def close(self):
        await self._async_client.aclose()

    async def aget(self, key: str) -> bytes:
        response = await self._async_client.post(
            "/cat", params={"arg": key}
        )
        response.raise_for_status()
        return response.content

    def get(self, key: str) -> bytes:
        response = self._client.post("/cat", params={"arg": key})
        response.raise_for_status()
        return response.content

    @overload
    async def aput(
        self, value: bytes, *, file_name: str | None = None
    ) -> str: ...  # pragma: no cover

    @overload
    async def aput(
        self, value: io.FileIO, *, file_name: str | None = None
    ) -> str: ...  # pragma: no cover

    async def aput(self, value, *, file_name) -> str:
        if file_name is None:
            file_name = uuid.uuid4().hex
        if isinstance(value, bytes):
            value = io.BytesIO(value)
        return await self._aput(value, file_name)

    async def _aput(self, file_: io.FileIO, file_name: str) -> str:
        files = {
            "file": (file_name, file_, "application/octet-stream")
        }
        response = await self._async_client.post("/add", files=files)
        response.raise_for_status()
        result = response.json()
        return result["Hash"]

    @overload
    async def put(
        self, value: bytes, *, file_name: str | None = None
    ) -> str: ...  # pragma: no cover

    @overload
    async def put(
        self, value: io.FileIO, *, file_name: str | None = None
    ) -> str: ...  # pragma: no cover

    def put(self, value, *, file_name) -> str:
        if file_name is None:
            file_name = uuid.uuid4().hex
        if isinstance(value, bytes):
            value = io.BytesIO(value)
        return self._put(value, file_name)

    def _put(self, file_: io.FileIO, file_name: str) -> str:
        files = {
            "file": (file_name, file_, "application/octet-stream")
        }
        response = self._client.post("/add", files=files)
        response.raise_for_status()
        result = response.json()
        return result["Hash"]
