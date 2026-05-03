from fastapi import APIRouter, HTTPException
from database.supabase_client import get_supabase

router = APIRouter(prefix="/api", tags=["catalog"])


# =========================================
# GET ALL CATEGORIES
# =========================================
@router.get("/categories")
async def get_categories():
    try:
        supabase = get_supabase()

        result = supabase.table("categories") \
            .select("*") \
            .order("name") \
            .execute()

        return {
            "success": True,
            "data": result.data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================
# GET ALL ITEMS (FLAT LIST)
# =========================================
@router.get("/items")
async def get_items():
    try:
        supabase = get_supabase()

        result = supabase.table("items") \
            .select("""
                id,
                name,
                price,
                unit,
                categories(name)
            """) \
            .execute()

        items = [
            {
                "id": item["id"],
                "name": item["name"],
                "price": item["price"],
                "unit": item["unit"],
                "category": item["categories"]["name"] if item.get("categories") else None
            }
            for item in result.data
        ]

        return {
            "success": True,
            "data": items
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================
# GET ITEMS BY CATEGORY
# =========================================
@router.get("/items/{category_name}")
async def get_items_by_category(category_name: str):
    try:
        supabase = get_supabase()

        # Step 1: get category id
        cat = supabase.table("categories") \
            .select("id") \
            .eq("name", category_name) \
            .single() \
            .execute()

        if not cat.data:
            raise HTTPException(status_code=404, detail="Category not found")

        category_id = cat.data["id"]

        # Step 2: get items
        result = supabase.table("items") \
            .select("name, price, unit") \
            .eq("category_id", category_id) \
            .order("name") \
            .execute()

        return {
            "success": True,
            "category": category_name,
            "data": result.data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================
# GET FULL CATALOG (BEST FOR FRONTEND)
# =========================================
@router.get("/catalog")
async def get_catalog():
    """
    Returns data in EXACT format your frontend expects:
    {
      Grocery: [{name, price, unit}],
      Fruits: [...]
    }
    """
    try:
        supabase = get_supabase()

        result = supabase.table("items") \
            .select("""
                name,
                price,
                unit,
                categories(name)
            """) \
            .execute()

        catalog = {}

        for item in result.data:
            category = item["categories"]["name"]

            if category not in catalog:
                catalog[category] = []

            catalog[category].append({
                "name": item["name"],
                "price": item["price"],
                "unit": item["unit"]
            })

        return {
            "success": True,
            "data": catalog
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================
# HEALTH CHECK
# =========================================
@router.get("/catalog/health")
async def catalog_health():
    return {
        "status": "ok",
        "service": "catalog"
    }