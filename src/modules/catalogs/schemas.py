from pydantic import BaseModel


class CatalogResponse(BaseModel):
    catalog_type: str
    items: dict[str, str]