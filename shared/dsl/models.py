from __future__ import annotations

from enum import Enum
from typing import Annotated, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, conint, constr


class TargetBy(str, Enum):
    ROLE = "role"
    LABEL = "label"
    PLACEHOLDER = "placeholder"
    TESTID = "testid"
    TEXT = "text"
    CSS = "css"
    XPATH = "xpath"
    VISION = "vision"


class TargetSpec(BaseModel):
    """Declarative selector bundle entry."""

    model_config = ConfigDict(extra="forbid")

    by: TargetBy
    role: Optional[str] = None
    name: Optional[str] = None
    text: Optional[str] = None
    css: Optional[str] = None
    xpath: Optional[str] = None
    placeholder: Optional[str] = None
    testid: Optional[str] = Field(default=None, alias="data-testid")
    near_text: Optional[str] = Field(default=None, alias="nearText")
    frame: Optional[str] = None
    index: Optional[int] = None


class WaitConditionKind(str, Enum):
    URL_CONTAINS = "url_contains"
    TEXT_PRESENT = "text_present"
    DOWNLOAD = "download"
    SELECTOR_VISIBLE = "selector_visible"
    TABLE_ROWS_GTE = "table_rows>="
    NETWORK_IDLE = "network_idle"


class WaitCondition(BaseModel):
    """Condition used by wait_for actions."""

    model_config = ConfigDict(extra="forbid")

    kind: WaitConditionKind
    value: Optional[Union[str, int]] = None
    filename_like: Optional[str] = None
    target: Optional[TargetSpec] = None


class ActionBase(BaseModel):
    """Base action type."""

    model_config = ConfigDict(extra="forbid")

    type: str
    requires_human: bool = False
    description: Optional[str] = None


class NavigateAction(ActionBase):
    type: Literal["navigate"]
    url: HttpUrl | constr(min_length=1)


class ClickAction(ActionBase):
    type: Literal["click"]
    target: TargetSpec


class FillAction(ActionBase):
    type: Literal["fill"]
    target: TargetSpec
    value: str


class SelectAction(ActionBase):
    type: Literal["select"]
    target: TargetSpec
    option: str


class PressAction(ActionBase):
    type: Literal["press"]
    keys: List[str]


class HoverAction(ActionBase):
    type: Literal["hover"]
    target: TargetSpec


class WaitForAction(ActionBase):
    type: Literal["wait_for"]
    condition: WaitCondition


class UploadAction(ActionBase):
    type: Literal["upload"]
    target: TargetSpec
    path: str


class ScrollViewportMode(str, Enum):
    INTO_VIEW = "into_view"
    TO_BOTTOM = "to_bottom"
    BY_OFFSET = "by_offset"


class ScrollAction(ActionBase):
    type: Literal["scroll"]
    target: Optional[TargetSpec] = None
    mode: ScrollViewportMode = ScrollViewportMode.INTO_VIEW
    offset_x: Optional[int] = Field(default=None, alias="x")
    offset_y: Optional[int] = Field(default=None, alias="y")


class ExtractAction(ActionBase):
    type: Literal["extract"]
    query: TargetSpec
    limit: Optional[int] = None


class ExecAction(ActionBase):
    type: Literal["exec"]
    script: str


class LoopAction(ActionBase):
    type: Literal["loop"]
    query: TargetSpec
    limit: Optional[int] = None
    body: List["Action"]


Action = Annotated[
    Union[
        NavigateAction,
        ClickAction,
        FillAction,
        SelectAction,
        PressAction,
        HoverAction,
        WaitForAction,
        UploadAction,
        ScrollAction,
        ExtractAction,
        ExecAction,
        LoopAction,
    ],
    Field(discriminator="type"),
]


class ActionProgram(BaseModel):
    """A complete DSL program emitted by the planner."""

    model_config = ConfigDict(extra="forbid")

    steps: List[Action] = Field(default_factory=list)
