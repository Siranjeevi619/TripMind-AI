from pydantic import BaseModel, Field


class QueryRouter(BaseModel):
    strategy : str = Field(
        description= "Retrieval strategy to use. "
            "Choose one of: vector, hybrid, multi_query."
        )

    