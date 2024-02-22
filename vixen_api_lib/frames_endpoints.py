from fastapi import Response, Path
from .api import api
from .globals import State_Response
from .features import Features
from .frames_models import Models
from .shared_models import SharedModels

# Frame IDs
@api.get(
        '/frames/{feature_name}/ids',
        description = 'Get the frame IDs of a feature',
        responses = {
            200: {'model': Models.FrameIds},
            404: {'model': SharedModels.KeyError},
        }
)
async def frame_ids(
    response: Response,
    feature_name: str = Path(description = 'Feature name'),
):
    if Features.key_exists(feature_name):
        feature = Features.get(feature_name)

        return State_Response(response, 200)(
            Models.FrameIds(
                frame_ids = feature.frame_ids,
                active_frame_ids = feature.active_frame_ids
            )
        )
    else:
        return State_Response(response, 404)(
            SharedModels.KeyError(
                message = f"Feature '{feature_name}' is not loaded",
                error = 'KeyError',
                key = feature_name
            )
        )

# Toggle Frame
@api.get(
        '/frame/{feature_name}/toggle/{frame_id}',
        description = 'Open or close a frame',
        responses = {
            200: {'model': Models.FrameState},
            404: {'model': SharedModels.KeyError}
        }
)
async def toggle_frame(
    response: Response,
    feature_name: str = Path(description = 'Feature name'),
    frame_id: str = Path(description = 'Frame id')
):
    if not Features.key_exists(feature_name):
        return State_Response(response, 404)(
            SharedModels.KeyError(
                message = f"Feature '{feature_name}' is not loaded",
                error = 'KeyError',
                key = feature_name
            )
        )

    feature = Features.get(feature_name)

    if frame_id in feature.active_frame_ids:
        feature.close_frame(frame_id)
        frame_opened = False
    elif frame_id in feature.frame_ids:
        frame_id = feature.open_frame(frame_id)
        frame_opened = True
    else:
        return State_Response(response, 404)(
            SharedModels.KeyError(
                message = f"Frame ID '{frame_id}' does not exist",
                error = 'KeyError',
                key = frame_id
            )
        )

    return State_Response(response, 200)(
        Models.FrameState(
            feature_name = feature_name,
            frame_id = frame_id,
            frame_opened = frame_opened
        )
    )

# Open Frame
@api.get(
        '/frame/{feature_name}/open/{frame_id}',
        description = 'Open a frame',
        responses = {
            200: {'model': Models.FrameState},
            404: {'model': SharedModels.KeyError},
            409: {'model': SharedModels.KeyError}
        }
)
async def open_frame(
    response: Response,
    feature_name: str = Path(description = 'Feature name'),
    frame_id: str = Path(description = 'Frame id')
):
    if not Features.key_exists(feature_name):
        return State_Response(response, 404)(
            SharedModels.KeyError(
                message = f"Feature '{feature_name}' is not loaded",
                error = 'KeyError',
                key = feature_name
            )
        )

    feature = Features.get(feature_name)

    if frame_id in feature.active_frame_ids:
        return State_Response(response, 409)(
            SharedModels.KeyError(
                message = f"Frame '{frame_id}' is already open",
                error = 'KeyExists',
                key = frame_id
            )
        )

    if not frame_id in feature.frame_ids:
        return State_Response(response, 404)(
            SharedModels.KeyError(
                message = f"Frame ID '{frame_id}' does not exist",
                error = 'KeyError',
                key = frame_id
            )
        )

    frame_id = feature.open_frame(frame_id)
    return State_Response(response, 200)(
        Models.FrameState(
            feature_name = feature_name,
            frame_id = frame_id,
            frame_opened = True
        )
    )

# Close Frame
@api.get(
        '/frame/{feature_name}/close/{frame_id}',
        description = 'Close a frame',
        responses = {
            200: {'model': Models.FrameState},
            404: {'model': SharedModels.KeyError},
            409: {'model': SharedModels.KeyError}
        }
)
async def open_frame(
    response: Response,
    feature_name: str = Path(description = 'Feature name'),
    frame_id: str = Path(description = 'Frame id')
):
    if not Features.key_exists(feature_name):
        return State_Response(response, 404)(
            SharedModels.KeyError(
                message = f"Feature '{feature_name}' is not loaded",
                error = 'KeyError',
                key = feature_name
            )
        )

    feature = Features.get(feature_name)

    if not frame_id in feature.active_frame_ids:
        return State_Response(response, 409)(
            SharedModels.KeyError(
                message = f"Frame '{frame_id}' is not open",
                error = 'KeyError',
                key = frame_id
            )
        )
    
    feature.close_frame(frame_id)
    return State_Response(response, 200)(
        Models.FrameState(
            feature_name = feature_name,
            frame_id = frame_id,
            frame_opened = False
        )
    )