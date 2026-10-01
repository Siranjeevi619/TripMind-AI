from pydantic import BaseModel


class MetaDataFiltering(BaseModel):
    city: str
    category: str