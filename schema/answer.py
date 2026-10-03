from dataclasses import Field

from pydantic import BaseModel


class Answer(BaseModel):
    answer : str = Field(
        description="Answer based only on the provided context."
    )

    grounded : bool = Field(
        description="Whether the answer is supported by the provided context."
    )