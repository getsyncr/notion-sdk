from typing import TYPE_CHECKING, Any, Union

from notion.helpers import parse_block_obj, pick
from notion.types import Block, BotUser, Database, Page, PaginatedList, PersonUser, User, UserType


if TYPE_CHECKING:
    from notion import NotionClient


class Endpoint:
    def __init__(self, client: "NotionClient") -> None:
        self.client = client


class BlocksChildrenEndpoint(Endpoint):
    def append(self, block_id: str, **kwargs) -> Block:
        return parse_block_obj(
            self.client.request(
                path="blocks/{id}/children".format(id=block_id),
                method="PATCH",
                body=pick(kwargs, "children"),
            )
        )

    def list(self, block_id: str, **kwargs) -> PaginatedList[Block]:
        return PaginatedList[Block].parse_obj(
            self.client.request(
                path="blocks/{id}/children".format(id=block_id),
                method="GET",
                auth=kwargs.get("auth", None),
                query=pick(kwargs, "start_cursor", "page_size"),
            )
        )


class BlocksEndpoint(Endpoint):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.children = BlocksChildrenEndpoint(*args, **kwargs)

    def retrieve(self, block_id: str, **kwargs) -> Block:
        return parse_block_obj(
            self.client.request(
                path="blocks/{id}".format(id=block_id),
                method="GET",
                auth=kwargs.get("auth", None),
            )
        )

    def update(self, block_id: str, **kwargs):
        return parse_block_obj(
            self.client.request(
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


class DatabasesEndpoint(Endpoint):
    def create(self, **kwargs) -> Database:
        return Database.parse_obj(
            self.client.request(
                method="POST",
                path="/databases",
                auth=kwargs.get("auth", None),
                query=pick(kwargs, "start_cursor"),
            )
        )

    def list(self, **kwargs) -> PaginatedList[Database]:
        return PaginatedList[Database].parse_obj(
            self.client.request(
                method="GET",
                path="/databases",
                auth=kwargs.get("auth", None),
                query=pick(kwargs, "start_cursor", "page_size"),
            )
        )

    def query(self, database_id: str, **kwargs) -> PaginatedList[Page]:
        return PaginatedList[Page].parse_obj(
            self.client.request(
                method="POST",
                path="/databases/{id}/query".format(id=database_id),
                auth=kwargs.get("auth", None),
                body=pick(kwargs, "filter", "sorts", "start_cursor", "page_size"),
            )
        )

    def retrieve(self, database_id: str, **kwargs) -> Database:
        return Database.parse_obj(
            self.client.request(
                method="GET",
                path="/databases/{id}".format(id=database_id),
                auth=kwargs.get("auth", None),
            )
        )


class PagesEndpoint(Endpoint):
    def create(self, **kwargs) -> Page:
        return Page.parse_obj(
            self.client.request(
                method="POST",
                path="/pages",
                auth=kwargs.get("auth", None),
                body=pick(kwargs, "parent", "properties", "children"),
            )
        )

    def retrieve(self, page_id: str, **kwargs) -> Page:
        return Page.parse_obj(
            self.client.request(
                method="GET",
                path="pages/{id}".format(id=page_id),
                auth=kwargs.get("auth", None),
            )
        )

    def update(self, page_id: str, **kwargs) -> Page:
        return Page.parse_obj(
            self.client.request(
                method="PATCH",
                path="pages/{id}".format(id=page_id),
                auth=kwargs.get("auth", None),
                body=pick(kwargs, "archived", "properties"),
            )
        )


class UsersEndpoint(Endpoint):
    def list(self, **kwargs) -> PaginatedList[User]:
        return PaginatedList[User].parse_obj(
            self.client.request(
                method="GET",
                path="/users",
                auth=kwargs.get("auth", None),
                query=pick(kwargs, "start_cursor", "page_size"),
            )
        )

    def retrieve(self, user_id: str, **kwargs) -> Union[BotUser, PersonUser]:
        response = self.client.request(
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


class SearchEndpoint(Endpoint):
    def __call__(self, **kwargs) -> PaginatedList[Union[Page, Database]]:
        return PaginatedList[Union[Page, Database]].parse_obj(
            self.client.request(
                path="/search",
                method="POST",
                auth=kwargs.get("auth", None),
                body=pick(kwargs, "query", "sort", "filter", "start_cursor", "page_size"),
            )
        )
