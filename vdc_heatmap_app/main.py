import sys
import uvicorn
from fastapi import FastAPI
from config import settings
from api.create_heatmap import heatmap_router

vdc_app = FastAPI()
configuration = settings.Settings(_env_file=".env", _env_file_encoding="utf-8")
# PORT
# HOST

# Import and include your route modules based on the environment
if configuration.is_testing:
    pass
    vdc_app.include_router(heatmap_router)
elif configuration.is_dev:
    # Add routes for the dev environment
    pass
elif configuration.is_prod:
    # Add routes for the prod environment
    pass

if __name__ == "__main__":
    try:
        uvicorn.run(vdc_app, host="0.0.0.0", port=8000)
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            f"The current module is not available {sys.path}"
        ) from e
