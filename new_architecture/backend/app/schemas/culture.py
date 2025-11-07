from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FolkCultureBase(BaseModel):
    name: str
    description: str
    region: str
    content: str
    image_url: Optional[str] = None

class FolkCultureCreate(FolkCultureBase):
    pass

class FolkCultureUpdate(FolkCultureBase):
    pass

class FolkCultureResponse(FolkCultureBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True