from fastapi import APIRouter, HTTPException
from models.heatmap_coordinates import Heatmap

heatmap_router = APIRouter()


@heatmap_router.post("/heatmap")
async def create_heatmap(input_data: Heatmap) -> dict[str, str]:
    try:
        input_data.generate_heatmap()
        # implemeent a validation to confirm that the heatmap has been created.

        return {
            "message": "Heatmap created successfully",
            "heatmap": input_data.image_id,
        }
    except ValueError as ve:
        # Catch validation error for 'heatmap' and return it as an HTTP error
        raise HTTPException(
            status_code=400, detail=f"Invalid 'heatmap' value: {ve}"
        ) from ve
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error generating heatmap") from e
