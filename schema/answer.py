
from pydantic import BaseModel, Field


class Answer(BaseModel):
    answer : str = Field(
        description="Answer based only on the provided context."
    )

    grounded : bool = Field(
        description="Whether the answer is supported by the provided context."
    )

    sources: list[str] = Field(
        description="Sources from the provided context that support the answer."
    )