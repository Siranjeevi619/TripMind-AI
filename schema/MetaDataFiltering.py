from typing import Literal

from pydantic import BaseModel


class MetaDataFiltering(BaseModel):
    city: str
    category: Literal["place", "event", "food"] = "place"
