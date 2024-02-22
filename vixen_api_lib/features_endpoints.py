from fastapi import Response, Path
from .api import api
from .globals import State_Response
from .features import Features
from .features_models import Models
from .shared_models import SharedModels

@api.get(
        '/feature/load/{feature_name}',
        description = 'Load a feature',
        responses = {
            200: {'model': Models.FeatureState},
            404: {'model': Models.FileNotFoundError},
            409: {'model': SharedModels.KeyError},
        }
)
async def load_feature(
    response: Response,
    feature_name: str = Path(description = 'Feature name'),
):
    try:
        if not Features.key_exists(feature_name):
            Features.load(feature_name)
            
            return State_Response(response, 200)(
                Models.FeatureState(
                    frame_name = feature_name,
                    is_loaded = True
                )
            )
        else:
            return State_Response(response, 409)(
                SharedModels.KeyError(
                    message = f"Feature '{feature_name}' is already loaded",
                    error = 'KeyExists',
                    key = feature_name
                )
            )
    except FileNotFoundError as error:
        return State_Response(response, 404)(
            Models.FileNotFoundError(
                message = f"Feature '{feature_name}' is not found",
                error = 'FileNotFound',
                filename = error.filename
            )
        )

@api.get(
        '/feature/unload/{feature_name}',
        description = 'Unload a feature',
        responses = {
            200: {'model': Models.FeatureState},
            404: {'model': SharedModels.KeyError}
        }
)
async def unload_feature(
    response: Response,
    feature_name: str = Path(description = 'Feature name')
):
    if Features.key_exists(feature_name):
        Features.unload(feature_name)

        return State_Response(response, 200)(
            Models.FeatureState(
                frame_name = feature_name,
                is_loaded = False
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