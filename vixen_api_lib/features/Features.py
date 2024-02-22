from typing import Dict
from .Feature import Feature

class Features:
    _features: Dict[str, Feature] = {}

    @staticmethod
    def load(feature_name: str):
        Features._features[feature_name] = Feature(feature_name)

    @staticmethod
    def unload(feature_name: str):
        if feature_name in Features._features:
            del Features._features[feature_name]

    @staticmethod
    def unload_all():
        feature_names = list(Features._features.keys())
        for feature_name in feature_names:
            Features.unload(feature_name)

    @staticmethod
    def key_exists(feature_name: str) -> bool:
        return feature_name in Features._features

    @staticmethod
    def get(feature_name: str) -> Feature:
        if feature_name in Features._features:
            return Features._features[feature_name]