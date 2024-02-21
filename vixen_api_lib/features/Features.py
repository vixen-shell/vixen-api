from typing import Dict
from .Feature import Feature

class Features:
    _features: Dict[str, Feature] = {}

    @staticmethod
    def open(feature_name: str):
        Features._features[feature_name] = Feature(feature_name)

    # @staticmethod
    # def close(feature_name: str):
    #     Features._features[feature_name].destroy_frames()
    #     del Features._features[feature_name]

    @staticmethod
    def get_feature(feature_name: str):
        return Features._features[feature_name]