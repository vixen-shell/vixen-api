from fastapi import HTTPException
from fastapi.responses import JSONResponse
from .api import api
from .clients_handler import clients_handler

@api.get('/client/{feature_name}/open')
async def open_client(feature_name: str):
    data = clients_handler.open(feature_name)
    if isinstance(data, HTTPException): raise data
    return JSONResponse(data)

@api.get('/client/{client_id}/close')
async def close_client(client_id: str):
    data = await clients_handler.close(client_id)
    if isinstance(data, HTTPException): raise data
    return JSONResponse(data)

@api.get('/client/{feature_name}/ids')
async def get_feature_client_ids(feature_name: str):
    data = clients_handler.get_feature_ids(feature_name)

    if not data:
        raise HTTPException(
            status_code = 404,
            detail = f"'{feature_name}' feature has no client!"
        )

    return JSONResponse(data)

@api.get('/client/ids')
async def get_client_ids():
    data = clients_handler.get_ids()

    if not data:
        raise HTTPException(
            status_code = 404,
            detail = f"No client ids found!"
        )

    return JSONResponse(data)