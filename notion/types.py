from datetime import datetime
from enum import Enum
from typing import Dict, Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from pydantic.networks import EmailStr, HttpUrl


APISingularObject = TypeVar("APISingularObject")


class Color(str, Enum):
    BLUE = "blue"
    BROWN = "brown"
    DEFAULT = "default"
    GRAY = "gray"
    GREEN = "green"
    ORANGE = "orange"
    PURPLE = "purple"
    PINK = "pink"
    RED = "red"
    YELLOW = "yellow"


class BackgroundColor(str, Enum):
    BLUE_BACKGROUND = "blue_background"
    BROWN_BACKGROUND = "brown_background"
    GRAY_BACKGROUND = "gray_background"
    GREEN_BACKGROUND = "green_background"
    ORANGE_BACKGROUND = "orange_background"
    PURPLE_BACKGROUND = "purple_background"
    PINK_BACKGROUND = "pink_background"
    RED_BACKGROUND = "red_background"
    YELLOW_BACKGROUND = "yellow_background"


class NumberFormat(str, Enum):
    DOMMAR = "dollar"
    EURO = "euro"
    NUMBER = "number"
    NUMBER_WITH_COMMAS = "number_with_commas"
    PERCENT = "percent"
    POUND = "pound"
    RUBLE = "ruble"
    RUPEE = "rupee"
    WON = "won"
    YEN = "yen"
    YUAN = "yuan"


class RollupFunction(str, Enum):
    COUNT_ALL = "count_all"
    COUNT_VALUES = "count_values"
    COUNT_UNIQUE_VALUES = "count_unique_values"
    COUNT_EMPTY = "count_empty"
    COUNT_NOT_EMPTY = "count_not_empty"
    PERCENT_EMPTY = "percent_empty"
    PERCENT_NOT_EMPTY = "percent_not_empty"
    SUM = "sum"
    AVERAGE = "average"
    MEDIAN = "median"
    MIN = "min"
    MAX = "max"
    RANGE = "range"
    SHOW_ORIGINAL = "show_original"


class Annotations(BaseModel):
    bold: bool
    italic: bool
    strikethrough: bool
    underline: bool
    code: bool
    color: Union[Color, BackgroundColor]


class RichTextBaseInput(BaseModel):
    plain_text: Optional[str]
    href: Optional[HttpUrl]
    annotations: Optional[Annotations]
    type: str


class PropertyBase(BaseModel):
    id: str
    type: str


class TitleProperty(PropertyBase):
    type: str = Field("title", const=True)
    title: Dict = Field({}, const=True)


class RichTextProperty(PropertyBase):
    type: str = Field("rich_text", const=True)
    rich_text: Dict = Field({}, const=True)


class Number(BaseModel):
    format: NumberFormat


class NumberProperty(PropertyBase):
    type: str = Field("number", const=True)
    number: Number


class SelectOptionBase(BaseModel):
    color: Optional[Color]


class SelectOptionWithName(SelectOptionBase):
    name: str


class SelectOptionWithId(SelectOptionBase):
    id: str


SelectOption = TypeVar("SelectOption", SelectOptionWithName, SelectOptionWithId)
MultiSelectOption = SelectOption


class Select(BaseModel):
    options: List[SelectOption]


class MultiSelect(BaseModel):
    options: List[MultiSelectOption]


class SelectProperty(PropertyBase):
    type: str = Field("select", const=True)
    select: Select


class MultipleSelectProperty(PropertyBase):
    type: str = Field("multi_select", const=True)
    multi_select: MultiSelect


class DateProperty(PropertyBase):
    type: str = Field("date", const=True)
    date: Dict = Field({}, const=True)


class PeopleProperty(PropertyBase):
    type: str = Field("people", const=True)
    people: Dict = Field({}, const=True)


class FilesProperty(PropertyBase):
    type: str = Field("files", const=True)
    file: Dict = Field({}, const=True)


class CheckboxProperty(PropertyBase):
    type: str = Field("checkbox", const=True)
    checkbox: Dict = Field({}, const=True)


class URLProperty(PropertyBase):
    type: str = Field("url", const=True)
    url: Dict = Field({}, const=True)


class EmailProperty(PropertyBase):
    type: str = Field("email", const=True)
    email: Dict = Field({}, const=True)


class PhoneNumberProperty(PropertyBase):
    type: str = Field("phone_number", const=True)
    phone_number: Dict = Field({}, const=True)


class Formula(BaseModel):
    expression: str


class FormulaProperty(PropertyBase):
    type: str = Field("formula", const=True)
    formula: Formula


class Relation(BaseModel):
    database_id: str
    synced_property_name: Optional[str]
    synced_property_id: Optional[str]


class RelationProperty(PropertyBase):
    type: str = Field("relation", const=True)
    relation: Relation


class Rollup(BaseModel):
    relation_property_name: str
    relation_property_id: str
    rollup_property_name: str
    rollup_property_id: str
    function: RollupFunction


class RollupProperty(PropertyBase):
    type: str = Field("rollup", const=True)
    rollup: Rollup


class CreatedTimeProperty(PropertyBase):
    type: str = Field("created_time", const=True)
    created_time: Dict = Field({}, const=True)


class CreatedByProperty(PropertyBase):
    type: str = Field("created_by", const=True)
    created_by: Dict = Field({}, const=True)


class LastEditedTimeProperty(PropertyBase):
    type: str = Field("last_edited_time", const=True)
    last_edited_time: Dict = Field({}, const=True)


class LastEditedByProperty(PropertyBase):
    type: str = Field("last_edited_by", const=True)
    last_edited_by: Dict = Field({}, const=True)


Property = TypeVar(
    "Property",
    TitleProperty,
    RichTextProperty,
    NumberProperty,
    SelectProperty,
    MultipleSelectProperty,
    DateProperty,
    PeopleProperty,
    FilesProperty,
    CheckboxProperty,
    URLProperty,
    EmailProperty,
    PhoneNumberProperty,
    RelationProperty,
    RollupProperty,
    CreatedTimeProperty,
    CreatedByProperty,
    LastEditedByProperty,
    LastEditedTimeProperty,
)


class BlockBase(BaseModel):
    object: str = Field("block", const=True)
    id: str
    type: str
    created_time: datetime
    last_edited_time: datetime
    has_children: bool


class Paragraph(BaseModel):
    children: Optional[List["Block"]]


class ParagraphBlock(BlockBase):
    type: str = Field("paragraph", const=True)
    paragraph: Paragraph


class HeadingOneBlock(BlockBase):
    type: str = Field("heading_1", const=True)
    has_children: bool = Field(False, const=True)


class HeadingTwoBlock(BlockBase):
    type: str = Field("heading_2", const=True)
    has_children: bool = Field(False, const=True)


class HeadingThreeBlock(BlockBase):
    type: str = Field("heading_3", const=True)
    has_children: bool = Field(False, const=True)


Block = TypeVar("Block", ParagraphBlock, HeadingOneBlock, HeadingTwoBlock, HeadingThreeBlock)


# Database Parent
# Reference: https://developers.notion.com/reference/page#database-parent


class ParentDatabase(BaseModel):
    type: str = Field("database_id", const=True)
    database_id: str


# Page Parent
# Reference: https://developers.notion.com/reference/page#page-parent


class ParentPage(BaseModel):
    type: str = Field("page_id", const=True)
    page_id: str


# Workspace Parent
# https://developers.notion.com/reference/page#workspace-parent


class ParentWorkspace(BaseModel):
    type: str = Field("workspace", const=True)
    workspace: bool = True


class Database(BaseModel):
    """
    Database object

    Database objects describe the property schema of a database in Notion.
    Pages are the items (or children) in a database.
    Page property values must conform to the property objects laid out in the parent database object.

    Reference: https://developers.notion.com/reference/database
    """

    object: str = Field("database", const=True)
    id: str
    parent: Union[ParentPage, ParentWorkspace]
    created_time: datetime
    last_edited_time: datetime
    properties: Dict[str, Property]


class Page(BaseModel):
    """
    Page object

    The Page object contains the property values of a single Notion page.
    All pages have a parent. If the parent is a database,
    the property values conform to the schema laid out database's properties.
    Otherwise, the only property value is the title.
    Page content is available as blocks.
    The content can be read using retrieve block children and appended using append block children.

    Reference: https://developers.notion.com/reference/page
    """

    object: str = Field("page", const=True)
    id: str
    parent: Union[ParentDatabase, ParentPage, ParentWorkspace]
    created_time: datetime
    last_edited_time: datetime
    archived: bool
    url: HttpUrl


class UserType(str, Enum):
    BOT = "bot"
    PERSON = "person"


class UserBase(BaseModel):
    object: str = Field("user", const=True)
    id: str
    type: Optional[str]
    name: str
    avatar_url: Optional[str]


class BotUser(UserBase):
    type: UserType = Field(UserType.BOT, const=True)


class Person(BaseModel):
    email: EmailStr


class PersonUser(UserBase):
    type: UserType = Field(UserType.PERSON, const=True)
    person: Optional[Person]


User = TypeVar("User", BotUser, PersonUser)


class PaginatedList(GenericModel, Generic[APISingularObject]):
    """
    Pagination object

    Endpoints which return a list of objects use pagination.
    Pagination allows an integration to request a part of the list,
    receiving an array of results and a next_cursor in the response.
    The integration can use the next_cursor in another request to receive the next part of the list.
    Using this technique, the integration can continue to make requests
    to receive the whole list (or just the parts the integration needs).

    Reference: https://developers.notion.com/reference/pagination
    """

    object: str = "list"
    results: List[APISingularObject]
    has_more: bool
    next_cursor: Optional[str] = None
