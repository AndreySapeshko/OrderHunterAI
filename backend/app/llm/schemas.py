from typing import List, Optional

from pydantic import BaseModel, Field


class Budget(BaseModel):
    min: Optional[int]
    max: Optional[int]
    currency: Optional[str]


class Requirements(BaseModel):
    tech_stack: list[str] = Field(default_factory=list)
    other: dict[str, str] = Field(default_factory=dict)


class LLMLeadResult(BaseModel):
    is_relevant: bool
    relevance_reason: str

    category: str

    requirements: Requirements
    stack: List[str] = Field(default_factory=list)

    budget: Optional[Budget]
    deadline_days: Optional[int]

    score: int = Field(ge=0, le=100)
