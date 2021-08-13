from typing import Any, Dict, Optional, Union

from httpx import (
    URL,
    AsyncClient,
    Client,
    Headers,
    HTTPStatusError,
    Request,
    Response,
    TimeoutException,
)

from notion import __version__
from notion.endpoints import (
    BlocksAsyncEndpoint,
    BlocksEndpoint,
    DatabasesAsyncEndpoint,
    DatabasesEndpoint,
    PagesAsyncEndpoint,
    PagesEndpoint,
    SearchAsyncEndpoint,
    SearchEndpoint,
    UsersAsyncEndpoint,
    UsersEndpoint,
)
from notion.errors import APIResponseError, HTTPResponseError, RequestTimeoutError, is_api_error


DEFAULT_NOTION_URL = "https://api.notion.com/v1/"
DEFAULT_NOTION_VERSION = "2021-05-13"
DEFAULT_NOTION_SDK_USER_AGENT = f"notion-sdk/{__version__} (https://github.com/getsyncr/notion-sdk)"


class BaseClient:
    def __init__(
        self,
        client: Union[Client, AsyncClient],
        auth: Optional[str] = None,
        timeout: int = 60,
        base_url: str = DEFAULT_NOTION_URL,
        notion_version: str = DEFAULT_NOTION_VERSION,
        user_agent: str = DEFAULT_NOTION_SDK_USER_AGENT,
    ) -> None:
        self.auth = auth
        if base_url and not base_url.endswith("/v1/"):
            base_url = base_url + "/v1/"
        self.base_url = URL(base_url)
        self.timeout = timeout
        self.notion_version = notion_version
        self.user_agent = user_agent

        self.client: Union[Client, AsyncClient] = client(
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

    def _build_request(
        self,
        method: str,
        path: str,
        query: Optional[Dict[Any, Any]] = None,
        body: Optional[Dict[Any, Any]] = None,
        auth: Optional[str] = None,
    ) -> Request:
        headers = Headers()
        if auth is not None:
            headers["Authorization"] = "Bearer {token}".format(token=auth)
        return self.client.build_request(method, path, params=query, json=body, headers=headers)

    def _parse_response(self, response: Response) -> Any:
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


class NotionClient(BaseClient):
    def __init__(
        self,
        auth: Optional[str] = None,
        timeout: int = 60,
        base_url: str = DEFAULT_NOTION_URL,
        notion_version: str = DEFAULT_NOTION_VERSION,
        user_agent: str = DEFAULT_NOTION_SDK_USER_AGENT,
    ) -> None:
        super().__init__(
            Client,
            auth=auth,
            timeout=timeout,
            base_url=base_url,
            notion_version=notion_version,
            user_agent=user_agent,
        )

        self.blocks = BlocksEndpoint(self)
        self.databases = DatabasesEndpoint(self)
        self.pages = PagesEndpoint(self)
        self.search = SearchEndpoint(self)
        self.users = UsersEndpoint(self)

    def request(
        self,
        method: str,
        path: str,
        auth: Optional[str] = None,
        query: Optional[Dict[Any, Any]] = None,
        body: Optional[Dict[Any, Any]] = None,
    ) -> Response:
        request = self._build_request(method, path, query=query, body=body, auth=auth)
        response = self.client.send(request)
        return self._parse_response(response)


class NotionAsyncClient(BaseClient):
    def __init__(
        self,
        auth: Optional[str] = None,
        timeout: int = 60,
        base_url: str = DEFAULT_NOTION_URL,
        notion_version: str = DEFAULT_NOTION_VERSION,
        user_agent: str = DEFAULT_NOTION_SDK_USER_AGENT,
    ) -> None:
        super().__init__(
            AsyncClient,
            auth=auth,
            timeout=timeout,
            base_url=base_url,
            notion_version=notion_version,
            user_agent=user_agent,
        )

        self.blocks = BlocksAsyncEndpoint(self)
        self.databases = DatabasesAsyncEndpoint(self)
        self.pages = PagesAsyncEndpoint(self)
        self.search = SearchAsyncEndpoint(self)
        self.users = UsersAsyncEndpoint(self)

    async def request(
        self,
        method: str,
        path: str,
        auth: Optional[str] = None,
        query: Optional[Dict[Any, Any]] = None,
        body: Optional[Dict[Any, Any]] = None,
    ) -> Response:
        request = self._build_request(method, path, query=query, body=body, auth=auth)
        async with self.client as client:
            response = await client.send(request)
        return self._parse_response(response)
