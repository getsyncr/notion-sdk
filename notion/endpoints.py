from typing import TYPE_CHECKING, Any, Union

from notion.helpers import pick
from notion.types import Block, BotUser, Database, Page, PaginatedList, PersonUser, User, UserType


if TYPE_CHECKING:
    from .client import Client


class Endpoint:
    def __init__(self, client: "Client") -> None:
        self.client = client


class BlocksChildrenEndpoint(Endpoint):
    async def append(self, block_id: str, **kwargs) -> Block:
        response = await self.client.request(
            path="blocks/{id}/children".format(id=block_id),
            method="PATCH",
            body=pick(
                kwargs,
                "children",
            ),
        )

        block_type = response.get("type", None)
        if block_type == "":
            return
        else:
            raise ValueError("")

    async def list(self, block_id: str, **kwargs) -> PaginatedList[Block]:
        return PaginatedList[Block].parse_obj(
            await self.client.request(
                path="blocks/{id}/children".format(id=block_id),
                method="GET",
                query=pick(
                    kwargs,
                    "start_cursor",
                    "page_size",
                ),
            )
        )


class BlocksEndpoint(Endpoint):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.children = BlocksChildrenEndpoint(*args, **kwargs)


class DatabasesEndpoint(Endpoint):
    async def create(self, **kwargs) -> Database:
        return Database.parse_obj(
            await self.client.request(
                method="POST",
                path="/databases",
                query=pick(
                    kwargs,
                    "start_cursor",
                ),
            )
        )

    async def list(self, **kwargs) -> PaginatedList[Database]:
        return PaginatedList[Database].parse_obj(
            await self.client.request(
                method="GET",
                path="/databases",
                query=pick(
                    kwargs,
                    "start_cursor",
                    "page_size",
                ),
            )
        )

    async def query(self, database_id: str, **kwargs) -> PaginatedList[Page]:
        return PaginatedList[Page].parse_obj(
            await self.client.request(
                method="POST",
                path="/databases/{id}/query".format(id=database_id),
                body=pick(
                    kwargs,
                    "filter",
                    "sorts",
                    "start_cursor",
                    "page_size",
                ),
            )
        )

    async def retrieve(self, database_id: str) -> Database:
        return Database.parse_obj(
            await self.client.request(
                method="GET",
                path="/databases/{id}".format(id=database_id),
            )
        )


class PagesEndpoint(Endpoint):
    async def create(self, **kwargs) -> Page:
        return Page.parse_obj(
            await self.client.request(
                method="POST",
                path="/pages",
                body=pick(
                    kwargs,
                    "parent",
                    "properties",
                    "children",
                ),
            )
        )

    async def retrieve(self, page_id: str, **kwargs) -> Page:
        return Page.parse_obj(
            await self.client.request(
                method="GET",
                path="pages/{id}".format(id=page_id),
            )
        )

    async def update(self, page_id: str, **kwargs) -> Page:
        return Page.parse_obj(
            await self.client.request(
                method="PATCH",
                path="pages/{id}".format(id=page_id),
                body=pick(
                    kwargs,
                    "archived",
                    "properties",
                ),
            )
        )


class UsersEndpoint(Endpoint):
    async def list(self, **kwargs) -> PaginatedList[User]:
        """
        Returns a paginated list of `Users` for the workspace.
        The response may contain fewer that `page_size` of results.

        :params start_cursor: If supplied will return a page of results starting after the cursor provided.
        If not supplied, this endpoint will return the first page of results.

        :params page_size: The number of items from the full list desired in the response. Maximum: 100
        """

        return PaginatedList[User].parse_obj(
            await self.client.request(
                method="GET",
                path="/users",
                query=pick(
                    kwargs,
                    "start_cursor",
                    "page_size",
                ),
            )
        )

    async def retrieve(self, user_id: str) -> Union[BotUser, PersonUser]:
        """
        Retrieves a `User` using the ID specified.

        :params user_id: Identifier for a Notion user
        """

        response = await self.client.request(
            method="GET",
            path="/users/{id}".format(id=user_id),
        )

        user_type = response.get("type", None)
        if user_type == UserType.BOT:
            return BotUser.parse_obj(response)
        elif user_type == UserType.PERSON:
            return PersonUser.parse_obj(response)
        else:
            raise ValueError("Could not decode User object with type {type}".format(type=user_type))


class SearchEndpoint(Endpoint):
    async def __call__(self, **kwargs) -> PaginatedList[Union[Page, Database]]:
        return PaginatedList[Union[Page, Database]].parse_obj(
            await self.client.request(
                path="/search",
                method="POST",
                body=pick(
                    kwargs,
                    "query",
                    "sort",
                    "filter",
                    "start_cursor",
                    "page_size",
                ),
            )
        )
