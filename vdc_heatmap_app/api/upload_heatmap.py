# Unnecessary at the moment. Will be instead made into part of the back-end service. 
# No endpoint needed to upload the image.

# from fastapi import APIRouter, HTTPException
# from ..models import Heatmap_Coordinates


# heatmap_router = APIRouter()

# @heatmap_router.post("/upload_image")
# async def upload_heatmap(input_data: ):
#     try:
#         result = heatmap_generator.heatmap_creator(input_data)
#         return {"heatmap": result}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Error generating heatmap") from e