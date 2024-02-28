from fastapi import Response, Path
from .api import api
from .globals import ModelResponses, CommonsModels, FeatureModels, FrameModels
from .features import Features

# Frame IDs
ids_responses = ModelResponses({
    200: FrameModels.FrameIds,
    404: CommonsModels.Error,
    409: CommonsModels.Error
})

@api.get(
        '/frames/{feature_name}/ids',
        description = 'Get the frame IDs of a feature',
        responses = ids_responses.responses
)
async def frame_ids(
    response: Response,
    feature_name: str = Path(description = 'Feature name'),
):
    if not Features.key_exists(feature_name):
        return ids_responses(response, 404)(
            message = f"Feature '{feature_name}' not found",
            details = CommonsModels.KeyError(
                key = feature_name
            )
        )
    
    feature = Features.get(feature_name)

    if not feature.is_started:
        return ids_responses(response, 409)(
            message = f"Feature '{feature_name}' is not started",
            details = FeatureModels.FeatureBase(
                name = feature_name,
                is_started = False
            )
        )

    return ids_responses(response, 200)(
        ids = feature.frame_ids,
        actives = feature.active_frame_ids
    )

# Toggle Frame
toggle_responses = ModelResponses({
    200: FrameModels.FrameProperty,
    404: CommonsModels.Error,
    409: CommonsModels.Error
})

@api.get(
        '/frame/{feature_name}/toggle/{frame_id}',
        description = 'Open or close a frame',
        responses = toggle_responses.responses
)
async def toggle_frame(
    response: Response,
    feature_name: str = Path(description = 'Feature name'),
    frame_id: str = Path(description = 'Frame id')
):
    if not Features.key_exists(feature_name):
        return toggle_responses(response, 404)(
            message = f"Feature '{feature_name}' not found",
            details = CommonsModels.KeyError(
                key = feature_name
            )
        )

    feature = Features.get(feature_name)

    if not feature.is_started:
        return toggle_responses(response, 409)(
            message = f"Feature '{feature_name}' is not started",
            details = FeatureModels.FeatureBase(
                name = feature_name,
                is_started = False
            )
        )

    if frame_id in feature.active_frame_ids:
        feature.close_frame(frame_id)
        frame_opened = False
    elif frame_id in feature.frame_ids:
        frame_id = feature.open_frame(frame_id)
        frame_opened = True
    else:
        return toggle_responses(response, 404)(
            message = f"Frame ID '{frame_id}' does not exist",
            details = CommonsModels.KeyError(
                key = frame_id
            )
        )

    return toggle_responses(response, 200)(
        id = frame_id,
        is_opened = frame_opened,
        feature = FeatureModels.FeatureBase(
            name = feature_name
        )
    )

# Open Frame
open_responses = ModelResponses({
    200: FrameModels.FrameProperty,
    404: CommonsModels.Error,
    409: CommonsModels.Error
})

@api.get(
        '/frame/{feature_name}/open/{frame_id}',
        description = 'Open a frame',
        responses = open_responses.responses
)
async def open_frame(
    response: Response,
    feature_name: str = Path(description = 'Feature name'),
    frame_id: str = Path(description = 'Frame id')
):
    if not Features.key_exists(feature_name):
        return open_responses(response, 404)(
            message = f"Feature '{feature_name}' not found",
            details = CommonsModels.KeyError(
                key = feature_name
            )
        )

    feature = Features.get(feature_name)

    if not feature.is_started:
        return open_responses(response, 409)(
            message = f"Feature '{feature_name}' is not started",
            details = FeatureModels.FeatureBase(
                name = feature_name,
                is_started = False
            )
        )

    if frame_id in feature.active_frame_ids:
        return open_responses(response, 409)(
            message = f"Frame '{frame_id}' is already open",
            details = FrameModels.FrameProperty(
                id = frame_id,
                feature = FeatureModels.FeatureBase(
                    name = feature_name
                )
            )
        )

    if not frame_id in feature.frame_ids:
        return open_responses(response, 404)(
            message = f"Frame ID '{frame_id}' does not exist",
            details = CommonsModels.KeyError(
                key = frame_id
            )
        )

    frame_id = feature.open_frame(frame_id)

    return open_responses(response, 200)(
        id = frame_id,
        feature = FeatureModels.FeatureBase(
            name = feature_name
        )
    )

# Close Frame
close_responses = ModelResponses({
    200: FrameModels.FrameProperty,
    404: CommonsModels.Error,
    409: CommonsModels.Error
})

@api.get(
        '/frame/{feature_name}/close/{frame_id}',
        description = 'Close a frame',
        responses = close_responses.responses
)
async def open_frame(
    response: Response,
    feature_name: str = Path(description = 'Feature name'),
    frame_id: str = Path(description = 'Frame id')
):
    if not Features.key_exists(feature_name):
        return close_responses(response, 404)(
            message = f"Feature '{feature_name}' not found",
            details = CommonsModels.KeyError(
                key = feature_name
            )
        )

    feature = Features.get(feature_name)

    if not feature.is_started:
        return close_responses(response, 409)(
            message = f"Feature '{feature_name}' is not started",
            details = FeatureModels.FeatureBase(
                name = feature_name,
                is_started = False
            )
        )

    if not frame_id in feature.active_frame_ids:
        return close_responses(response, 409)(
            message = f"Frame '{frame_id}' is not open",
            details = FrameModels.FrameProperty(
                id = frame_id,
                is_opened = False,
                feature = FeatureModels.FeatureBase(
                    name = feature_name
                )
            )

        )
    
    feature.close_frame(frame_id)

    return close_responses(response, 200)(
        id = frame_id,
        is_opened = False,
        feature = FeatureModels.FeatureBase(
            name = feature_name
        )
    )