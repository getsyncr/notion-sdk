from typing import TYPE_CHECKING, Any, Union

from notion.helpers import parse_block_obj, pick
from notion.types import Block, BotUser, Database, Page, PaginatedList, PersonUser, User, UserType


if TYPE_CHECKING:
    from notion.client import NotionAsyncClient


class AsyncEndpoint:
    def __init__(self, client: "NotionAsyncClient") -> None:
        self.client = client


class BlocksChildrenAsyncEndpoint(AsyncEndpoint):
    async def append(self, block_id: str, **kwargs) -> Block:
        return parse_block_obj(
            await self.client.request(
                path="blocks/{id}/children".format(id=block_id),
                method="PATCH",
                body=pick(kwargs, "children"),
            )
        )

    async def list(self, block_id: str, **kwargs) -> PaginatedList[Block]:
        return PaginatedList[Block].parse_obj(
            await self.client.request(
                path="blocks/{id}/children".format(id=block_id),
                method="GET",
                auth=kwargs.get("auth", None),
                query=pick(kwargs, "start_cursor", "page_size"),
            )
        )


class BlocksAsyncEndpoint(AsyncEndpoint):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.children = BlocksChildrenAsyncEndpoint(*args, **kwargs)

    async def retrieve(self, block_id: str, **kwargs) -> Block:
        return parse_block_obj(
            await self.client.request(
                path="blocks/{id}".format(id=block_id),
                method="GET",
                auth=kwargs.get("auth", None),
            )
        )

    async def update(self, block_id: str, **kwargs):
        return parse_block_obj(
            await self.client.request(
                path="blocks/{id}".format(id=block_id),
                method="PATCH",
                auth=kwargs.get("auth", None),
                body=pick(
                    kwargs,
                    "paragraph",
                    "heading_1",
                    "heading_2",
                    "heading_3",
                    "bulleted_list_item",
                    "numbered_list_item",
                    "toggle",
                    "to_do",
                ),
            )
        )


class DatabasesAsyncEndpoint(AsyncEndpoint):
    async def create(self, **kwargs) -> Database:
        return Database.parse_obj(
            await self.client.request(
                method="POST",
                path="/databases",
                auth=kwargs.get("auth", None),
                query=pick(kwargs, "start_cursor"),
            )
        )

    async def list(self, **kwargs) -> PaginatedList[Database]:
        return PaginatedList[Database].parse_obj(
            await self.client.request(
                method="GET",
                path="/databases",
                auth=kwargs.get("auth", None),
                query=pick(kwargs, "start_cursor", "page_size"),
            )
        )

    async def query(self, database_id: str, **kwargs) -> PaginatedList[Page]:
        return PaginatedList[Page].parse_obj(
            await self.client.request(
                method="POST",
                path="/databases/{id}/query".format(id=database_id),
                auth=kwargs.get("auth", None),
                body=pick(kwargs, "filter", "sorts", "start_cursor", "page_size"),
            )
        )

    async def retrieve(self, database_id: str, **kwargs) -> Database:
        return Database.parse_obj(
            await self.client.request(
                method="GET",
                path="/databases/{id}".format(id=database_id),
                auth=kwargs.get("auth", None),
            )
        )


class PagesAsyncEndpoint(AsyncEndpoint):
    async def create(self, **kwargs) -> Page:
        return Page.parse_obj(
            await self.client.request(
                method="POST",
                path="/pages",
                auth=kwargs.get("auth", None),
                body=pick(kwargs, "parent", "properties", "children"),
            )
        )

    async def retrieve(self, page_id: str, **kwargs) -> Page:
        return Page.parse_obj(
            await self.client.request(
                method="GET",
                path="pages/{id}".format(id=page_id),
                auth=kwargs.get("auth", None),
            )
        )

    async def update(self, page_id: str, **kwargs) -> Page:
        return Page.parse_obj(
            await self.client.request(
                method="PATCH",
                path="pages/{id}".format(id=page_id),
                auth=kwargs.get("auth", None),
                body=pick(kwargs, "archived", "properties"),
            )
        )


class UsersAsyncEndpoint(AsyncEndpoint):
    async def list(self, **kwargs) -> PaginatedList[User]:
        return PaginatedList[User].parse_obj(
            await self.client.request(
                method="GET",
                path="/users",
                auth=kwargs.get("auth", None),
                query=pick(kwargs, "start_cursor", "page_size"),
            )
        )

    async def retrieve(self, user_id: str, **kwargs) -> Union[BotUser, PersonUser]:
        response = await self.client.request(
            method="GET",
            path="/users/{id}".format(id=user_id),
            auth=kwargs.get("auth", None),
        )

        user_type = response.get("type", None)
        if user_type == UserType.BOT:
            return BotUser.parse_obj(response)
        elif user_type == UserType.PERSON:
            return PersonUser.parse_obj(response)
        else:
            raise ValueError("Could not decode User object with type {type}".format(type=user_type))


class SearchAsyncEndpoint(AsyncEndpoint):
    async def __call__(self, **kwargs) -> PaginatedList[Union[Page, Database]]:
        return PaginatedList[Union[Page, Database]].parse_obj(
            await self.client.request(
                path="/search",
                method="POST",
                auth=kwargs.get("auth", None),
                body=pick(kwargs, "query", "sort", "filter", "start_cursor", "page_size"),
            )
        )
