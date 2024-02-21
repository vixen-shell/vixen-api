from fastapi import HTTPException
from fastapi.responses import JSONResponse
from .api import api
from .features import Features

@api.get('/feature/{feature_name}/open')
async def open_feature(feature_name: str):
    Features.open(feature_name)