from datetime import date, datetime
from enum import Enum
from typing import Dict, Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from pydantic.networks import EmailStr, HttpUrl


APISingularObject = TypeVar("APISingularObject")


class NotionObjectType(str, Enum):
    BLOCK = "block"
    DATABASE = "database"
    PAGE = "page"
    USER = "user"


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
    RUPIAH = "rupiah"
    LIRA = "lira"
    REAL = "real"
    FRANC = "franc"
    CANADIAN_DOLLAR = "canadian_dollar"
    HONG_KONG_DOLLAR = "hong_kong_dollar"
    NEW_ZEALAND_DOLLAR = "new_zealand_dollar"
    KRONA = "krona"
    NORWEGIAN_KRONE = "norwegian_krone"
    MEXICAN_PESO = "mexican_peso"
    RAND = "rand"
    NEW_TAIWAN_DOLLAR = "new_taiwan_dollar"
    DANISH_KRONE = "danish_krone"
    ZLOTY = "zloty"
    BAHT = "baht"
    FORINT = "forint"
    KORUNA = "koruna"
    SHEKEL = "shekel"
    CHILEAN_PESO = "chilean_peso"
    PHILIPPINE_PESO = "philippine_peso"
    DIRHAM = "dirham"
    COLOMBIAN_PESO = "colombian_peso"
    RIYAL = "riyal"
    RINGGIT = "ringgit"
    LEU = "leu"


class RollupFunction(str, Enum):
    COUNT_ALL = "count_all"
    COUNT_VALUES = "count_values"
    COUNT_UNIQUE_VALUES = "count_unique_values"
    COUNT_EMPTY = "count_empty"
    COUNT_NOT_EMPTY = "count_not_empty"
    PERCENT_CHECKED = "percent_checked"
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
    object: str = Field(NotionObjectType.USER, const=True)
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


class PropertyType(str, Enum):
    CHECKBOX = "checkbox"
    CREATED_BY = "created_by"
    CREATED_TIME = "created_time"
    DATE = "date"
    EMAIL = "email"
    NUMBER = "number"
    MULTI_SELECT = "multi_select"
    PHONE_NUMBER = "phone_number"
    PEOPLE = "people"
    RICH_TEXT = "rich_text"
    SELECT = "select"
    TITLE = "title"
    FILES = "files"
    FORMULA = "formula"
    URL = "url"
    RELATION = "relation"
    ROLLUP = "rollup"
    LAST_EDITED_BY = "last_edited_by"
    LAST_EDITED_TIME = "last_edited_time"


class PropertyBase(BaseModel):
    id: str
    type: str
    name: str

    def get_configuration(self) -> Optional["PropertyConfiguration"]:
        """
        Returns configuration for given Property

        Utils method to get additional configuration values
        associated with a Property.
        Documentation for Property configuration is available here:
        https://developers.notion.com/reference/database#database-property
        """

        return getattr(self, str(self.type))


class TitleProperty(PropertyBase):
    type: str = Field(PropertyType.TITLE, const=True)
    title: Dict = Field({}, const=True)


class RichTextProperty(PropertyBase):
    type: str = Field(PropertyType.RICH_TEXT, const=True)
    rich_text: Dict = Field({}, const=True)


class Number(BaseModel):
    format: NumberFormat


class NumberProperty(PropertyBase):
    type: str = Field(PropertyType.NUMBER, const=True)
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
    type: str = Field(PropertyType.SELECT, const=True)
    select: Select


class MultipleSelectProperty(PropertyBase):
    type: str = Field(PropertyType.MULTI_SELECT, const=True)
    multi_select: MultiSelect


class DateProperty(PropertyBase):
    type: str = Field(PropertyType.DATE, const=True)
    date: Dict = Field({}, const=True)


class PeopleProperty(PropertyBase):
    type: str = Field(PropertyType.PEOPLE, const=True)
    people: Dict = Field({}, const=True)


class FilesProperty(PropertyBase):
    type: str = Field(PropertyType.FILES, const=True)
    file: Dict = Field({}, const=True)


class CheckboxProperty(PropertyBase):
    type: str = Field(PropertyType.CHECKBOX, const=True)
    checkbox: Dict = Field({}, const=True)


class URLProperty(PropertyBase):
    type: str = Field(PropertyType.URL, const=True)
    url: Dict = Field({}, const=True)


class EmailProperty(PropertyBase):
    type: str = Field(PropertyType.EMAIL, const=True)
    email: Dict = Field({}, const=True)


class PhoneNumberProperty(PropertyBase):
    type: str = Field(PropertyType.PHONE_NUMBER, const=True)
    phone_number: Dict = Field({}, const=True)


class Formula(BaseModel):
    expression: str


class FormulaProperty(PropertyBase):
    type: str = Field(PropertyType.FORMULA, const=True)
    formula: Formula


class Relation(BaseModel):
    database_id: str
    synced_property_name: Optional[str]
    synced_property_id: Optional[str]


class RelationProperty(PropertyBase):
    type: str = Field(PropertyType.RELATION, const=True)
    relation: Relation


class Rollup(BaseModel):
    relation_property_name: str
    relation_property_id: str
    rollup_property_name: str
    rollup_property_id: str
    function: RollupFunction


class RollupProperty(PropertyBase):
    type: str = Field(PropertyType.ROLLUP, const=True)
    rollup: Rollup


class CreatedTimeProperty(PropertyBase):
    type: str = Field(PropertyType.CREATED_TIME, const=True)
    created_time: Dict = Field({}, const=True)


class CreatedByProperty(PropertyBase):
    type: str = Field(PropertyType.CREATED_BY, const=True)
    created_by: Dict = Field({}, const=True)


class LastEditedTimeProperty(PropertyBase):
    type: str = Field(PropertyType.LAST_EDITED_TIME, const=True)
    last_edited_time: Dict = Field({}, const=True)


class LastEditedByProperty(PropertyBase):
    type: str = Field(PropertyType.LAST_EDITED_BY, const=True)
    last_edited_by: Dict = Field({}, const=True)


PropertyConfiguration = TypeVar(
    "PropertyConfiguration", Number, Select, MultiSelect, Formula, Relation, Rollup
)

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
    FormulaProperty,
)


class BlockType(str, Enum):
    PARAGRAPH = "paragraph"
    HEADING_ONE = "heading_1"
    HEADING_TWO = "heading_2"
    HEADING_THREE = "heading_3"
    BULLETED_LIST_ITEM = "bulleted_list_item"
    NUMBERED_LIST_ITEM = "numbered_list_item"
    TODO = "to_do"
    TOGGLE = "toggle"
    CHILD_PAGE = "child_page"
    UNSUPPORTED = "unsupported"


class BlockBase(BaseModel):
    object: str = Field(NotionObjectType.BLOCK, const=True)
    id: str
    type: str
    created_time: datetime
    last_edited_time: datetime
    has_children: bool


class Paragraph(BaseModel):
    text: List[RichText]
    children: Optional[List["Block"]]


class ParagraphBlock(BlockBase):
    type: str = Field(BlockType.PARAGRAPH, const=True)
    paragraph: Paragraph


class Heading(BaseModel):
    text: List[RichText]


class HeadingOneBlock(BlockBase):
    type: str = Field(BlockType.HEADING_ONE, const=True)
    heading_1: Heading
    has_children: bool = Field(False, const=True)


class HeadingTwoBlock(BlockBase):
    type: str = Field(BlockType.HEADING_TWO, const=True)
    heading_2: Heading
    has_children: bool = Field(False, const=True)


class HeadingThreeBlock(BlockBase):
    type: str = Field(BlockType.HEADING_THREE, const=True)
    heading_3: Heading
    has_children: bool = Field(False, const=True)


class BulletedListItem(BaseModel):
    text: List[RichText]
    children: Optional[List["Block"]]


class BulletedListItemBlock(BlockBase):
    type: str = Field(BlockType.BULLETED_LIST_ITEM, const=True)
    bulleted_list_item: BulletedListItem


class NumberedListItem(BaseModel):
    text: List[RichText]
    children: Optional[List["Block"]]


class NumberedListItemBlock(BlockBase):
    type: str = Field(BlockType.NUMBERED_LIST_ITEM, const=True)
    numbered_list_item: NumberedListItem


class Todo(BaseModel):
    text: List[RichText]
    checked: bool
    children: Optional[List["Block"]]


class ToDoBlock(BlockBase):
    type: str = Field(BlockType.TODO, const=True)
    to_do: Todo


class Toggle(BaseModel):
    text: List[RichText]
    children: Optional[List["Block"]]


class ToggleBlock(BlockBase):
    type: str = Field(BlockType.TOGGLE, const=True)
    toggle: Toggle


class ChildPage(BaseModel):
    title: str


class ChildPageBlock(BlockBase):
    type: str = Field(BlockType.CHILD_PAGE, const=True)
    child_page: ChildPage


class UnsupportedBlock(BlockBase):
    type: str = Field(BlockType.UNSUPPORTED, const=True)


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

BLOCK_MAPPING: Dict[BlockType, Block] = {
    BlockType.PARAGRAPH: ParagraphBlock,
    BlockType.HEADING_ONE: HeadingOneBlock,
    BlockType.HEADING_TWO: HeadingTwoBlock,
    BlockType.HEADING_THREE: HeadingThreeBlock,
    BlockType.BULLETED_LIST_ITEM: BulletedListItemBlock,
    BlockType.NUMBERED_LIST_ITEM: NumberedListItemBlock,
    BlockType.TODO: ToDoBlock,
    BlockType.TOGGLE: ToggleBlock,
    BlockType.CHILD_PAGE: ChildPageBlock,
    BlockType.UNSUPPORTED: UnsupportedBlock,
}


class ParentType(str, Enum):
    DATABASE = "database_id"
    PAGE = "page_id"
    WORKSPACE = "workspace"


class ParentDatabase(BaseModel):
    type: str = Field(ParentType.DATABASE, const=True)
    database_id: str


class ParentPage(BaseModel):
    type: str = Field(ParentType.PAGE, const=True)
    page_id: str


class ParentWorkspace(BaseModel):
    type: str = Field(ParentType.WORKSPACE, const=True)
    workspace: bool = True


class Database(BaseModel):
    object: str = Field(NotionObjectType.DATABASE, const=True)
    id: str
    parent: Union[ParentPage, ParentWorkspace]
    created_time: datetime
    last_edited_time: datetime
    title: List[RichText]
    properties: Dict[str, Property]


class PropertyValueType(str, Enum):
    ARRAY = "array"
    BOOLEAN = "boolean"
    CHECKBOX = "checkbox"
    CREATED_BY = "created_by"
    CREATED_TIME = "created_time"
    DATE = "date"
    EMAIL = "email"
    NUMBER = "number"
    MULTI_SELECT = "multi_select"
    PHONE_NUMBER = "phone_number"
    PEOPLE = "people"
    RICH_TEXT = "rich_text"
    SELECT = "select"
    TITLE = "title"
    FILES = "files"
    FORMULA = "formula"
    URL = "url"
    RELATION = "relation"
    ROLLUP = "rollup"
    LAST_EDITED_BY = "last_edited_by"
    LAST_EDITED_TIME = "last_edited_time"
    STR = "str"


class PropertyValueBase(BaseModel):
    id: str
    type: PropertyValueType


class TitlePropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.TITLE, const=True)
    title: List[RichText]


class RichTextPropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.RICH_TEXT, const=True)
    rich_text: List[RichText]


class TitleInputPropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.TITLE, const=True)
    title: List["RichTextInput"]


class RichTextInputPropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.RICH_TEXT, const=True)
    rich_text: List["RichTextInput"]


class NumberPropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.NUMBER, const=True)
    number: Union[int, float]


class SelectPropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.SELECT, const=True)
    select: SelectOption


class MultiSelectPropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.MULTI_SELECT, const=True)
    multi_select: List[MultiSelectOption]


class StartEndDate(BaseModel):
    start: date
    end: Optional[date]


class DatePropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.DATE, const=True)
    date: StartEndDate


class StringFormulaValue(BaseModel):
    type: PropertyValueType = Field(PropertyValueType.STR, const=True)
    str: Optional[str]


class NumberFormulaValue(BaseModel):
    type: PropertyValueType = Field(PropertyValueType.NUMBER, const=True)
    number: Optional[Union[int, float]]


class BooleanFormulaValue(BaseModel):
    type: PropertyValueType = Field(PropertyValueType.BOOLEAN, const=True)
    boolean: bool


class DateFormulaValue(BaseModel):
    type: PropertyValueType = Field(PropertyValueType.DATE, const=True)
    date: Optional[DatePropertyValue]


class FormulaPropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.FORMULA, const=True)
    formula: Union[StringFormulaValue, NumberFormulaValue, BooleanFormulaValue, DateFormulaValue]


class NumberRollupValue(BaseModel):
    type: PropertyValueType = Field(PropertyValueType.NUMBER, const=True)
    number: Union[int, float]


class DateRollupValue(BaseModel):
    type: PropertyValueType = Field(PropertyValueType.DATE, const=True)
    date: DatePropertyValue


class ArrayRollupValue(BaseModel):
    type: PropertyValueType = Field(PropertyValueType.ARRAY, const=True)
    array: List["PropertyValueWithoutId"]


class RollupPropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.ROLLUP, const=True)
    rollup: Union[NumberRollupValue, DateRollupValue, ArrayRollupValue]


class PeoplePropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.PEOPLE, const=True)
    people: List[User]


class FileName(BaseModel):
    name: str


class FilesPropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.FILES, const=True)
    files: List[FileName]


class CheckboxPropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.CHECKBOX, const=True)
    checkbox: bool


class URLPropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.URL, const=True)
    url: str


class EmailPropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.EMAIL, const=True)
    email: str


class PhoneNumberPropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.PHONE_NUMBER, const=True)
    phone_number: str


class CreatedTimePropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.CREATED_TIME, const=True)
    created_time: datetime


class CreatedByPropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.CREATED_BY, const=True)
    created_by: User


class LastEditedTimePropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.LAST_EDITED_TIME, const=True)
    last_edited_time: datetime


class LastEditedByPropertyValue(PropertyValueBase):
    type: PropertyValueType = Field(PropertyValueType.LAST_EDITED_BY, const=True)
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
    object: str = Field(NotionObjectType.PAGE, const=True)
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


class TextContentUpdate(BaseModel):
    text: List[RichTextInput]


class ParagraphUpdateBlock(BaseModel):
    paragraph: TextContentUpdate


class HeadingOneUpdateBlock(BaseModel):
    heading_1: TextContentUpdate


class HeadingTwoUpdateBlock(BaseModel):
    heading_2: TextContentUpdate


class HeadingThreeUpdateBlock(BaseModel):
    heading_3: TextContentUpdate


class BulletedListItemUpdateBlock(BaseModel):
    bulleted_list_item: TextContentUpdate


class NumberedListItemUpdateBlock(BaseModel):
    numbered_list_item: TextContentUpdate


class ToggleUpdateBlock(BaseModel):
    toggle: TextContentUpdate


class TodoUpdate(BaseModel):
    text: Optional[List[RichTextInput]]
    checked: Optional[bool]


class ToDoUpdateBlock(BaseModel):
    to_do: TodoUpdate


UpdateBlock = TypeVar(
    "UpdateBlock",
    ParagraphUpdateBlock,
    HeadingOneUpdateBlock,
    HeadingTwoUpdateBlock,
    HeadingThreeUpdateBlock,
    BulletedListItemUpdateBlock,
    NumberedListItemUpdateBlock,
    ToggleUpdateBlock,
    ToDoUpdateBlock,
)
