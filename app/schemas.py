from pydantic import BaseModel, Field
from typing import Literal


# Data coming from the support agent
class SupportRequest(BaseModel):
    customer_id: int = Field(gt=0)

    question: str = Field(
        min_length=5,
        max_length=500
    )

    product: str = Field(
        min_length=2,
        max_length=100
    )


# Data returned by our API
class SupportResponse(BaseModel):
    answer: str

    decision: Literal[
        "ANSWER",
        "HUMAN_REVIEW"
    ]

    reason: str

    # Multiple chunks may support one answer
    evidence: list[str]

    source: str | None = None
    policy_version: str | None = None

    # This is Chroma distance — lower means closer
    retrieval_distance: float | None = None