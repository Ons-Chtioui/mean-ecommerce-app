import os
import uuid
import mimetypes
from datetime import datetime, timezone
from typing import Any
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from motor.motor_asyncio import AsyncIOMotorDatabase

from database import get_database
from schemas.category import CategoryResponse
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
from config import settings

router = APIRouter(prefix="/products", tags=["products"])

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def _validate_object_id(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except (InvalidId, Exception):
        raise HTTPException(status_code=422, detail="Invalid id format")


def _category_doc_to_response(doc: dict) -> CategoryResponse:
    return CategoryResponse(
        id=str(doc["_id"]),
        name=doc["name"],
        description=doc.get("description", ""),
        createdAt=doc.get("createdAt", datetime.now(timezone.utc)),
        updatedAt=doc.get("updatedAt", datetime.now(timezone.utc)),
    )


async def _populate_product(doc: dict, db: AsyncIOMotorDatabase) -> dict:
    """Populate the category field of a product document."""
    cat_doc = await db["categories"].find_one({"_id": doc["category"]})
    if cat_doc:
        doc["category"] = _category_doc_to_response(cat_doc).model_dump()
    else:
        doc["category"] = {
            "id": str(doc["category"]),
            "name": "Unknown",
            "description": "",
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc),
        }
    return doc


def _doc_to_response(doc: dict) -> ProductResponse:
    return ProductResponse(
        id=str(doc["_id"]),
        name=doc["name"],
        description=doc.get("description", ""),
        price=doc.get("price", 0.0),
        image=doc.get("image", ""),
        category=doc["category"],  # already populated dict
        stock=doc.get("stock", 0),
        published=doc.get("published", True),
        rating=doc.get("rating", 0.0),
        createdAt=doc.get("createdAt", datetime.now(timezone.utc)),
        updatedAt=doc.get("updatedAt", datetime.now(timezone.utc)),
    )


# ── Upload endpoint (must be before /{id} to avoid route conflict) ──────────

@router.post("/upload")
async def upload_product_image(file: UploadFile = File(...)) -> Any:
    # Validate MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Read and validate size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds limit")

    # Save file
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(file.filename or "image.jpg")[1] or ".jpg"
    filename = f"product-{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(contents)

    return {"success": True, "data": {"file_path": f"/api/uploads/{filename}"}}


# ── Filter by category (must be before /{id}) ───────────────────────────────

@router.get("/category/{id}")
async def get_products_by_category(
    id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> Any:
    oid = _validate_object_id(id)
    docs = await db["products"].find({"category": oid}).to_list(length=None)
    populated = [await _populate_product(d, db) for d in docs]
    data = [_doc_to_response(d).model_dump() for d in populated]
    return {"success": True, "count": len(data), "data": data}


# ── CRUD ─────────────────────────────────────────────────────────────────────

@router.post("", status_code=201)
async def create_product(
    payload: ProductCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> Any:
    # Validate category exists
    cat_oid = _validate_object_id(payload.category)
    cat = await db["categories"].find_one({"_id": cat_oid})
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")

    now = datetime.now(timezone.utc)
    doc = {
        "name": payload.name,
        "description": payload.description,
        "price": payload.price,
        "image": payload.image,
        "category": cat_oid,
        "stock": payload.stock,
        "published": payload.published,
        "rating": payload.rating,
        "createdAt": now,
        "updatedAt": now,
    }
    result = await db["products"].insert_one(doc)
    created = await db["products"].find_one({"_id": result.inserted_id})
    populated = await _populate_product(created, db)
    return {
        "success": True,
        "message": "Product created successfully",
        "data": _doc_to_response(populated).model_dump(),
    }


@router.get("")
async def get_all_products(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> Any:
    docs = await db["products"].find().to_list(length=None)
    populated = [await _populate_product(d, db) for d in docs]
    data = [_doc_to_response(d).model_dump() for d in populated]
    return {"success": True, "count": len(data), "data": data}


@router.get("/{id}")
async def get_product(
    id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> Any:
    oid = _validate_object_id(id)
    doc = await db["products"].find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Product not found")
    populated = await _populate_product(doc, db)
    return {"success": True, "data": _doc_to_response(populated).model_dump()}


@router.put("/{id}")
async def update_product(
    id: str,
    payload: ProductUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> Any:
    oid = _validate_object_id(id)
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}

    if "category" in update_data:
        cat_oid = _validate_object_id(update_data["category"])
        cat = await db["categories"].find_one({"_id": cat_oid})
        if not cat:
            raise HTTPException(status_code=404, detail="Category not found")
        update_data["category"] = cat_oid

    if not update_data:
        raise HTTPException(status_code=422, detail="No valid fields to update")

    update_data["updatedAt"] = datetime.now(timezone.utc)
    result = await db["products"].find_one_and_update(
        {"_id": oid},
        {"$set": update_data},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    populated = await _populate_product(result, db)
    return {
        "success": True,
        "message": "Product updated successfully",
        "data": _doc_to_response(populated).model_dump(),
    }


@router.delete("/{id}")
async def delete_product(
    id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> Any:
    oid = _validate_object_id(id)
    result = await db["products"].find_one_and_delete({"_id": oid})
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"success": True, "message": "Product deleted successfully"}
