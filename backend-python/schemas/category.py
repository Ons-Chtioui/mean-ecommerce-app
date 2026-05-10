from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: str = Field(default="")


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    id: str
    name: str
    description: str
    createdAt: datetime
    updatedAt: datetime

    model_config = ConfigDict(populate_by_name=True)
