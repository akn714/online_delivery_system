from fastapi import APIRouter, HTTPException
from database.supabase_client import get_supabase

router = APIRouter(prefix="/api", tags=["config"])


# =========================================
# GET CONFIGURATION
# =========================================
@router.get("/config")
async def get_config():
    """
    Get delivery configuration (delivery charge and delivery status).
    """
    try:
        supabase = get_supabase()

        result = supabase.table("config") \
            .select("delivery_charge, is_delivery_closed") \
            .eq("id", 1) \
            .execute()

        if not result.data:
            # Return default values if no config found
            return {
                "success": True,
                "data": {
                    "delivery_charge": 15,
                    "is_delivery_closed": False
                }
            }

        config = result.data[0]
        return {
            "success": True,
            "data": {
                "delivery_charge": config["delivery_charge"],
                "is_delivery_closed": config["is_delivery_closed"].lower() == "true"
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================
# UPDATE CONFIGURATION (Admin only)
# =========================================
@router.put("/config")
async def update_config(delivery_charge: int = None, is_delivery_closed: bool = None):
    """
    Update delivery configuration (admin endpoint).
    """
    try:
        supabase = get_supabase()

        update_data = {}
        if delivery_charge is not None:
            update_data["delivery_charge"] = delivery_charge
        if is_delivery_closed is not None:
            update_data["is_delivery_closed"] = str(is_delivery_closed).lower()

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        result = supabase.table("config") \
            .update(update_data) \
            .eq("id", 1) \
            .execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Config not found")

        config = result.data[0]
        return {
            "success": True,
            "data": {
                "delivery_charge": config["delivery_charge"],
                "is_delivery_closed": config["is_delivery_closed"].lower() == "true"
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))