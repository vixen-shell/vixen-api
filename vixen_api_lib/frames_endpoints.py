from fastapi import HTTPException
from fastapi.responses import JSONResponse
from .api import api
from .features import Features

@api.get('/frames/{feature_name}/ids')
async def frame_ids(feature_name: str):
    return Features.get_feature(feature_name).frame_ids

@api.get('/frames/{feature_name}/actives')
async def active_frame_ids(feature_name: str):
    return Features.get_feature(feature_name).active_frame_ids

@api.get('/frame/{feature_name}/{frame_id}')
async def toggle_frame(feature_name: str, frame_id: str):
    feature = Features.get_feature(feature_name)

    if frame_id in feature.active_frame_ids:
        feature.close_frame(frame_id)
    else:
        feature.open_frame(frame_id)

@api.get('/frame/{feature_name}/{frame_id}/open')
async def open_frame(feature_name: str, frame_id: str):
    Features.get_feature(feature_name).open_frame(frame_id)

@api.get('/frame/{feature_name}/{frame_id}/close')
async def close_frame(feature_name: str, frame_id: str):
    Features.get_feature(feature_name).close_frame(frame_id)