from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from schemas.category import CategoryResponse


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str
    price: float = Field(..., ge=0)
    category: str  # category ObjectId as string
    stock: int = Field(default=0, ge=0)
    image: str = Field(default="")
    published: bool = Field(default=True)
    rating: float = Field(default=0.0, ge=0, le=5)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    category: Optional[str] = None
    stock: Optional[int] = Field(None, ge=0)
    image: Optional[str] = None
    published: Optional[bool] = None
    rating: Optional[float] = Field(None, ge=0, le=5)


class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    price: float
    image: str
    category: CategoryResponse  # always populated
    stock: int
    published: bool
    rating: float
    createdAt: datetime
    updatedAt: datetime

    model_config = ConfigDict(populate_by_name=True)
