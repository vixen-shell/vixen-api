from fastapi import Response, Path
from .api import api
from .globals import ModelResponses, CommonsModels, FeatureModels
from .features import Features

# FEATURE NAMES
names_responses = ModelResponses({
    200: FeatureModels.FeatureNames
})

@api.get(
        '/features/names',
        description = 'Get active feature names',
        responses = names_responses.responses
)
async def start_feature(response: Response):
    return names_responses(response, 200)(
        names = Features.keys()
    )

# START FEATURE
start_responses = ModelResponses({
    200: FeatureModels.FeatureBase,
    404: CommonsModels.Error,
    409: CommonsModels.Error
})

@api.get(
        '/feature/{feature_name}/start',
        description = 'Start a feature',
        responses = start_responses.responses
)
async def start_feature(
    response: Response,
    feature_name: str = Path(description = 'Feature name'),
):
    if not Features.key_exists(feature_name):
        return start_responses(response, 404)(
            message = f"Feature '{feature_name}' not found",
            details = CommonsModels.KeyError(
                key = feature_name
            )
        )
    
    feature = Features.get(feature_name)
    
    if feature.is_started:
        return start_responses(response, 409)(
            message = f"Feature '{feature_name}' is already started",
            details = FeatureModels.FeatureBase(
                name = feature_name
            )
        )
    
    feature.start()

    return start_responses(response, 200)(
        name = feature_name
    )

# STOP FEATURE
stop_responses = ModelResponses({
    200: FeatureModels.FeatureBase,
    404: CommonsModels.Error,
    409: CommonsModels.Error
})

@api.get(
        '/feature/{feature_name}/stop',
        description = 'Stop a feature',
        responses = stop_responses.responses
)
async def unload_feature(
    response: Response,
    feature_name: str = Path(description = 'Feature name')
):
    if not Features.key_exists(feature_name):
        return stop_responses(response, 404)(
            message = f"Feature '{feature_name}' not found",
            details = CommonsModels.KeyError(
                key = feature_name
            )
        )
    
    feature = Features.get(feature_name)

    if not feature.is_started:
        return stop_responses(response, 409)(
            message = f"Feature '{feature_name}' is not started",
            details = FeatureModels.FeatureBase(
                name = feature_name,
                is_started = False
            )
        )

    await feature.stop()

    return stop_responses(response, 200)(
        name = feature_name,
        is_started = False
    )

# STATE FEATURE
state_responses = ModelResponses({
    200: FeatureModels.FeatureState,
    404: CommonsModels.Error,
    409: CommonsModels.Error
})

@api.get(
        '/feature/{feature_name}/state',
        description = 'Get a feature state',
        responses = state_responses.responses
)
async def state_feature(
    response: Response,
    feature_name: str = Path(description = 'Feature name')
):
    if not Features.key_exists(feature_name):
        return state_responses(response, 404)(
            message = f"Feature '{feature_name}' not found",
            details = CommonsModels.KeyError(
                key = feature_name
            )
        )
    
    feature = Features.get(feature_name)

    if not feature.is_started:
        return state_responses(response, 409)(
            message = f"Feature '{feature_name}' is not started",
            details = FeatureModels.FeatureBase(
                name = feature_name,
                is_started = False
            )
        )

    return state_responses(response, 200)(
        name = feature_name,
        is_started = True,
        state = feature.state
    )