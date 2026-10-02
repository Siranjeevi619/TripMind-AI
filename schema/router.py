from pydantic import Field


class QueryRouter:
    strategy : str = Field(
        description= "Retrieval strategy to use. "
            "Choose one of: vector, hybrid, multi_query."
        )

    