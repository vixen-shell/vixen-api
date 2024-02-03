from .api import api
from .features import start_feature

@api.get('/{feature}/start')
async def start_feature_handler(feature):
    start_feature(feature)