from .LayerSetting import LayerSetting

class FrameSetting:
    def __init__(self, feature_name: str, frame_data: dict):
        self.id = frame_data['id']
        self.feature = feature_name
        self.title = frame_data.get('title') or frame_data['id']
        self.route = frame_data.get('route')
        self.instantiable = frame_data.get('instantiable') or False
        self.show_on_startup = frame_data.get('show_on_startup') or False

        layer_data = frame_data.get('layer')
        self.layer = LayerSetting(self.title, layer_data) if layer_data else None