from fastapi import Response, Path
from pydantic import BaseModel
from .api import api
from .features import Features

class OpenCloseResponse(BaseModel):
    key: str
    status: str

class FileNotFoundErrorResponse(BaseModel):
    message: str
    error: str
    filename: str

class KeyErrorResponse(BaseModel):
    message: str
    error: str
    key: str

@api.get(
        '/feature/{feature_name}/open',
        description = 'Load a feature',
        responses = {
            200: {'model': OpenCloseResponse},
            404: {'model': FileNotFoundErrorResponse}
        }
)
async def open_feature(
    response: Response,
    feature_name: str = Path(description = 'Feature name'),
):
    try:
        Features.open(feature_name)

        return OpenCloseResponse(
            key = feature_name,
            status = 'open'
        )
    except FileNotFoundError as error:
        response.status_code = 404

        return FileNotFoundErrorResponse(
            message = f"Feature '{feature_name}' not found",
            error = error.strerror,
            filename = error.filename
        )

@api.get(
        '/feature/{feature_name}/close',
        description = 'Unload a feature',
        responses = {
            200: {'model': OpenCloseResponse},
            404: {'model': KeyErrorResponse}
        }
)
async def close_feature(
    response: Response,
    feature_name: str = Path(description = 'Feature name')
):
    try:
        Features.close(feature_name)

        return OpenCloseResponse(
            key = feature_name,
            status = 'close'
        )
    except KeyError as error:
        response.status_code = 404

        return KeyErrorResponse(
            message = f"Feature '{feature_name}' not open",
            error = 'KeyError',
            key = str(error).strip("'")
        )