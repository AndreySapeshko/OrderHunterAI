from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Budget(BaseModel):
    min: Optional[int]
    max: Optional[int]
    currency: Optional[str]


class LLMLeadResult(BaseModel):
    is_relevant: bool
    relevance_reason: str

    category: str

    requirements: Dict[str, str] = Field(default_factory=dict)
    stack: List[str] = Field(default_factory=list)

    budget: Optional[Budget]
    deadline_days: Optional[int]

    score: int = Field(ge=0, le=100)
