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


class PaginatedList(GenericModel, Generic[APISingularObject]):
    object: str = "list"
    results: List[APISingularObject]
    has_more: bool
    next_cursor: Optional[str] = None


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


class Text(BaseModel):
    content: str
    link: Optional[HttpUrl]


class RichTextTextInput(RichTextBaseInput):
    type: str = Field("text", const=True)
    text: Text


class RichTextBase(RichTextBaseInput):
    plain_text: str
    annotations: Annotations


class RichTextText(RichTextTextInput):
    plain_text: str
    annotations: Annotations


class Mention(BaseModel):
    id: str


class DatabaseMention(BaseModel):
    type: str = Field("database", const=True)
    database: Mention


class DateMention(BaseModel):
    type: str = Field("date", const=True)


class PageMention(BaseModel):
    type: str = Field("page", const=True)
    page: Mention


class UserMention(BaseModel):
    type: str = Field("user", const=True)
    user: User


class RichTextMention(RichTextBase):
    type: str = Field("mention", const=True)
    mention: Union[UserMention, PageMention, DatabaseMention, DateMention]


class Equation(BaseModel):
    expression: str


class RichTextEquation(RichTextBase):
    type: str = Field("equation", const=True)
    equation: Equation


RichText = TypeVar("RichText", RichTextText, RichTextMention, RichTextEquation)
RichTextInput = TypeVar("RichTextInput", RichTextTextInput, RichTextMention, RichTextEquation)


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
    text: List[RichText]
    children: Optional[List["Block"]]


class ParagraphBlock(BlockBase):
    type: str = Field("paragraph", const=True)
    paragraph: Paragraph


class Heading(BaseModel):
    text: List[RichText]


class HeadingOneBlock(BlockBase):
    type: str = Field("heading_1", const=True)
    heading_1: Heading
    has_children: bool = Field(False, const=True)


class HeadingTwoBlock(BlockBase):
    type: str = Field("heading_2", const=True)
    heading_2: Heading
    has_children: bool = Field(False, const=True)


class HeadingThreeBlock(BlockBase):
    type: str = Field("heading_3", const=True)
    heading_3: Heading
    has_children: bool = Field(False, const=True)


class BulletedListItem(BaseModel):
    text: List[RichText]
    children: Optional[List["Block"]]


class BulletedListItemBlock(BlockBase):
    type: str = Field("bulleted_list_item", const=True)
    bulleted_list_item: BulletedListItem


class NumberedListItem(BaseModel):
    text: List[RichText]
    children: Optional[List["Block"]]


class NumberedListItemBlock(BlockBase):
    type: str = Field("numbered_list_item", const=True)
    numbered_list_item: NumberedListItem


class Todo(BaseModel):
    text: List[RichText]
    checked: bool
    children: Optional[List["Block"]]


class ToDoBlock(BlockBase):
    type: str = Field("to_do", const=True)
    to_do: Todo


class Toggle(BaseModel):
    text: List[RichText]
    children: Optional[List["Block"]]


class ToggleBlock(BlockBase):
    type: str = Field("toggle", const=True)
    toggle: Toggle


class ChildPage(BaseModel):
    title: str


class ChildPageBlock(BlockBase):
    type: str = Field("child_page", const=True)
    child_page: ChildPage


class UnsupportedBlock(BlockBase):
    type: str = Field("unsupported", const=True)


Block = TypeVar(
    "Block",
    ParagraphBlock,
    HeadingOneBlock,
    HeadingTwoBlock,
    HeadingThreeBlock,
    BulletedListItemBlock,
    NumberedListItemBlock,
    ToDoBlock,
    ToggleBlock,
    ChildPageBlock,
    UnsupportedBlock,
)


class ParentDatabase(BaseModel):
    type: str = Field("database_id", const=True)
    database_id: str


class ParentPage(BaseModel):
    type: str = Field("page_id", const=True)
    page_id: str


class ParentWorkspace(BaseModel):
    type: str = Field("workspace", const=True)
    workspace: bool = True


class Database(BaseModel):
    object: str = Field("database", const=True)
    id: str
    parent: Union[ParentPage, ParentWorkspace]
    created_time: datetime
    last_edited_time: datetime
    title: List[RichText]
    properties: Dict[str, Property]


class PropertyValueBase(BaseModel):
    id: str
    type: str


class TitlePropertyValue(PropertyValueBase):
    type: str = Field("title", const=True)
    title: List[RichText]


class RichTextPropertyValue(PropertyValueBase):
    type: str = Field("rich_text", const=True)
    rich_text: List[RichText]


class TitleInputPropertyValue(PropertyValueBase):
    type: str = Field("title", const=True)
    title: List["RichTextInput"]


class RichTextInputPropertyValue(PropertyValueBase):
    type: str = Field("rich_text", const=True)
    rich_text: List["RichTextInput"]


class NumberPropertyValue(PropertyValueBase):
    type: str = Field("number", const=True)
    number: Union[int, float]


class SelectPropertyValue(PropertyValueBase):
    type: str = Field("select", const=True)
    select: SelectOption


class MultiSelectPropertyValue(PropertyValueBase):
    type: str = Field("multi_select", const=True)
    multi_select: List[MultiSelectOption]


class StartEndDate(BaseModel):
    start: datetime
    end: Optional[datetime]


class DatePropertyValue(PropertyValueBase):
    type: str = Field("date", const=True)
    date: StartEndDate


class StringFormulaValue(BaseModel):
    type: str = Field("str", const=True)
    str: Optional[str]


class NumberFormulaValue(BaseModel):
    type: str = Field("number", const=True)
    number: Optional[Union[int, float]]


class BooleanFormulaValue(BaseModel):
    type: str = Field("boolean", const=True)
    boolean: bool


class DateFormulaValue(BaseModel):
    type: str = Field("date", const=True)
    date: DatePropertyValue


class FormulaPropertyValue(PropertyValueBase):
    type: str = Field("formula", const=True)
    formula: Union[StringFormulaValue, NumberFormulaValue, BooleanFormulaValue, DateFormulaValue]


class NumberRollupValue(BaseModel):
    type: str = Field("number", const=True)
    number: Union[int, float]


class DateRollupValue(BaseModel):
    type: str = Field("date", const=True)
    date: DatePropertyValue


class ArrayRollupValue(BaseModel):
    type: str = Field("array", const=True)
    array: List["PropertyValueWithoutId"]


class RollupPropertyValue(PropertyValueBase):
    type: str = Field("rollup", const=True)
    rollup: Union[NumberRollupValue, DateRollupValue, ArrayRollupValue]


class PeoplePropertyValue(PropertyValueBase):
    type: str = Field("people", const=True)
    people: List[User]


class FileName(BaseModel):
    name: str


class FilesPropertyValue(PropertyValueBase):
    type: str = Field("files", const=True)
    files: List[FileName]


class CheckboxPropertyValue(PropertyValueBase):
    type: str = Field("checkbox", const=True)
    checkbox: bool


class URLPropertyValue(PropertyValueBase):
    type: str = Field("url", const=True)
    url: str


class EmailPropertyValue(PropertyValueBase):
    type: str = Field("email", const=True)
    email: str


class PhoneNumberPropertyValue(PropertyValueBase):
    type: str = Field("phone_number", const=True)
    phone_number: str


class CreatedTimePropertyValue(PropertyValueBase):
    type: str = Field("created_time", const=True)
    created_time: datetime


class CreatedByPropertyValue(PropertyValueBase):
    type: str = Field("created_by", const=True)
    created_by: User


class LastEditedTimePropertyValue(PropertyValueBase):
    type: str = Field("last_edited_time", const=True)
    last_edited_time: datetime


class LastEditedByPropertyValue(PropertyValueBase):
    type: str = Field("last_edited_by", const=True)
    last_edited_by: User


PropertyValue = TypeVar(
    "PropertyValue",
    TitlePropertyValue,
    RichTextPropertyValue,
    NumberPropertyValue,
    SelectPropertyValue,
    MultiSelectPropertyValue,
    DatePropertyValue,
    FormulaPropertyValue,
    RollupPropertyValue,
    PeoplePropertyValue,
    FilesPropertyValue,
    CheckboxPropertyValue,
    URLPropertyValue,
    EmailPropertyValue,
    PhoneNumberPropertyValue,
    CreatedTimePropertyValue,
    CreatedByPropertyValue,
    LastEditedTimePropertyValue,
    LastEditedByPropertyValue,
)

InputPropertyValueWithRequiredId = TypeVar(
    "InputPropertyValueWithRequiredId",
    TitleInputPropertyValue,
    RichTextInputPropertyValue,
    NumberPropertyValue,
    SelectPropertyValue,
    MultiSelectPropertyValue,
    DatePropertyValue,
    FormulaPropertyValue,
    RollupPropertyValue,
    PeoplePropertyValue,
    FilesPropertyValue,
    CheckboxPropertyValue,
    URLPropertyValue,
    EmailPropertyValue,
    PhoneNumberPropertyValue,
    CreatedTimePropertyValue,
    CreatedByPropertyValue,
    LastEditedTimePropertyValue,
    LastEditedByPropertyValue,
)


class PropertyValueWithoutId(Generic[PropertyValue]):
    class Config:
        fields = {"id": {"exclude": True}}


class Page(BaseModel):
    object: str = Field("page", const=True)
    id: str
    parent: Union[ParentDatabase, ParentPage, ParentWorkspace]
    created_time: datetime
    last_edited_time: datetime
    archived: bool
    properties: Dict[str, PropertyValue]
    url: HttpUrl


class TitlePropertySchema(BaseModel):
    title: Dict = Field({}, const=True)


class RichTextPropertySchema(BaseModel):
    rich_text: Dict = Field({}, const=True)


class NumberOptionalFormat(BaseModel):
    format: Optional[NumberFormat]


class NumberPropertySchema(BaseModel):
    number: NumberOptionalFormat


class SelectOptionSchema(BaseModel):
    name: str
    color: Optional[Color]


MultiSelectOptionSchema = SelectOptionSchema


class SelectOptional(BaseModel):
    options: Optional[List[SelectOption]]


class MultiSelectOptional(BaseModel):
    options: Optional[List[MultiSelectOption]]


class SelectPropertySchema(BaseModel):
    select: SelectOptional


class MultiSelectPropertySchema(BaseModel):
    multi_select: MultiSelectOptional


class DatePropertySchema(BaseModel):
    date: Dict = Field({}, const=True)


class PeoplePropertySchema(BaseModel):
    people: Dict = Field({}, const=True)


class FilePropertySchema(BaseModel):
    files: Dict = Field({}, const=True)


class CheckboxPropertySchema(BaseModel):
    checkbox: Dict = Field({}, const=True)


class URLPropertySchema(BaseModel):
    url: Dict = Field({}, const=True)


class EmailPropertySchema(BaseModel):
    email: Dict = Field({}, const=True)


class PhoneNumberPropertySchema(BaseModel):
    phone_number: Dict = Field({}, const=True)


class CreatedTimePropertySchema(BaseModel):
    created_time: Dict = Field({}, const=True)


class CreatedByPropertySchema(BaseModel):
    created_by: Dict = Field({}, const=True)


class LastEditedTimePropertySchema(BaseModel):
    last_edited_time: Dict = Field({}, const=True)


class LastEditedByPropertySchema(BaseModel):
    last_edited_by: Dict = Field({}, const=True)


PropertySchema = TypeVar(
    "PropertySchema",
    TitlePropertySchema,
    RichTextPropertySchema,
    NumberPropertySchema,
    SelectPropertySchema,
    MultiSelectPropertySchema,
    DatePropertySchema,
    PeoplePropertySchema,
    FilePropertySchema,
    CheckboxPropertySchema,
    URLPropertySchema,
    EmailPropertySchema,
    PhoneNumberPropertySchema,
    CreatedTimePropertySchema,
    CreatedByPropertySchema,
    LastEditedTimePropertySchema,
    LastEditedByPropertySchema,
)
