from datetime import datetime, timezone
from typing import Any
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError

from database import get_database
from schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["categories"])


def _doc_to_response(doc: dict) -> CategoryResponse:
    """Convert a MongoDB document to a CategoryResponse."""
    return CategoryResponse(
        id=str(doc["_id"]),
        name=doc["name"],
        description=doc.get("description", ""),
        createdAt=doc.get("createdAt", datetime.now(timezone.utc)),
        updatedAt=doc.get("updatedAt", datetime.now(timezone.utc)),
    )


def _validate_object_id(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except (InvalidId, Exception):
        raise HTTPException(status_code=422, detail="Invalid id format")


@router.post("", status_code=201)
async def create_category(
    payload: CategoryCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> Any:
    now = datetime.now(timezone.utc)
    doc = {
        "name": payload.name,
        "description": payload.description,
        "createdAt": now,
        "updatedAt": now,
    }
    try:
        result = await db["categories"].insert_one(doc)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Name already exists")

    created = await db["categories"].find_one({"_id": result.inserted_id})
    return {
        "success": True,
        "message": "Category created successfully",
        "data": _doc_to_response(created).model_dump(),
    }


@router.get("")
async def get_all_categories(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> Any:
    docs = await db["categories"].find().to_list(length=None)
    data = [_doc_to_response(d).model_dump() for d in docs]
    return {"success": True, "count": len(data), "data": data}


@router.get("/{id}")
async def get_category(
    id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> Any:
    oid = _validate_object_id(id)
    doc = await db["categories"].find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"success": True, "data": _doc_to_response(doc).model_dump()}


@router.put("/{id}")
async def update_category(
    id: str,
    payload: CategoryUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> Any:
    oid = _validate_object_id(id)
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=422, detail="No valid fields to update")

    update_data["updatedAt"] = datetime.now(timezone.utc)
    try:
        result = await db["categories"].find_one_and_update(
            {"_id": oid},
            {"$set": update_data},
            return_document=True,
        )
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Name already exists")

    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    return {
        "success": True,
        "message": "Category updated successfully",
        "data": _doc_to_response(result).model_dump(),
    }


@router.delete("/{id}")
async def delete_category(
    id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> Any:
    oid = _validate_object_id(id)
    result = await db["categories"].find_one_and_delete({"_id": oid})
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"success": True, "message": "Category deleted successfully"}
