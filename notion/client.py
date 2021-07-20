from typing import Any, Dict, Optional

from httpx import URL, AsyncClient, Headers, HTTPStatusError, Response, TimeoutException

from notion.endpoints import (
    BlocksEndpoint,
    DatabasesEndpoint,
    PagesEndpoint,
    SearchEndpoint,
    UsersEndpoint,
)
from notion.errors import APIResponseError, HTTPResponseError, RequestTimeoutError, is_api_error


DEFAULT_NOTION_URL = "https://api.notion.com/v1/"
DEFAULT_NOTION_VERSION = "2021-05-13"


class Client:
    def __init__(
        self,
        auth: Optional[str] = None,
        timeout: int = 60,
        base_url: str = DEFAULT_NOTION_URL,
        notion_version: str = None,
        user_agent: str = None,
    ) -> None:
        self.auth = auth
        if base_url and not base_url.endswith("/v1/"):
            base_url = base_url + "/v1/"
        self.base_url = URL(base_url or DEFAULT_NOTION_URL)
        self.timeout = timeout
        self.notion_version = notion_version or DEFAULT_NOTION_VERSION
        self.user_agent = user_agent or "notionsdk-py"

        self.client = AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=Headers(
                {
                    "Notion-Version": self.notion_version,
                    "User-Agent": self.user_agent,
                }
            ),
        )

        if self.auth:
            self.client.headers["Authorization"] = "Bearer {token}".format(token=self.auth)

        self.blocks = BlocksEndpoint(self)
        self.databases = DatabasesEndpoint(self)
        self.pages = PagesEndpoint(self)
        self.search = SearchEndpoint(self)
        self.users = UsersEndpoint(self)

    async def request(
        self,
        method: str,
        path: str,
        auth: Optional[str] = None,
        query: Optional[Dict[Any, Any]] = None,
        body: Optional[Dict[Any, Any]] = None,
    ) -> Response:
        headers = Headers()
        if auth is not None:
            headers["Authorization"] = "Bearer {token}".format(token=auth)
        request = self.client.build_request(method, path, params=query, json=body, headers=headers)
        async with self.client as client:
            response = await client.send(request)
        try:
            response.raise_for_status()
        except TimeoutException:
            raise RequestTimeoutError()
        except HTTPStatusError as err:
            body = err.response.json()
            code = body.get("code", None)
            if is_api_error(code):
                raise APIResponseError(response, body["message"], code)
            raise HTTPResponseError(err.response)
        return response.json()
