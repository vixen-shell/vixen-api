import os

HOME_DIRECTORY = os.path.expanduser('~')
VX_CONFIG_DIRECTORY = f'{HOME_DIRECTORY}/.config/vixen'
FEATURE_SETTINGS_DIRECTORY = f'{VX_CONFIG_DIRECTORY}/features'
DEFAULT_FEATURES_CONFIG_FILE = f'{VX_CONFIG_DIRECTORY}/default_features.json'
FRONT_URL = 'http://localhost:6492'