from typing import List
from ...layerise import Edges, Levels, Margins

anchor_setting_values = {
    'top_start': [Edges.top, Edges.left],
    'top_center': [Edges.top],
    'top_end': [Edges.top, Edges.right],
    'top_stretch': [Edges.top, Edges.left, Edges.right],

    'right_start': [Edges.right, Edges.top],
    'right_center': [Edges.right],
    'right_end': [Edges.right, Edges.bottom],
    'right_stretch': [Edges.right, Edges.top, Edges.bottom],

    'bottom_start': [Edges.bottom, Edges.left],
    'bottom_center': [Edges.bottom],
    'bottom_end': [Edges.bottom, Edges.right],
    'bottom_stretch': [Edges.bottom, Edges.left, Edges.right],

    'left_start': [Edges.left, Edges.top],
    'left_center': [Edges.left],
    'left_end': [Edges.left, Edges.bottom],
    'left_stretch': [Edges.left, Edges.top, Edges.bottom],

    'full_center': None,
    'full_stretch': [Edges.top, Edges.right, Edges.bottom, Edges.left]
}

def set_level(data_value: str | None):
    try: return getattr(Levels, data_value)
    except: return None

def set_anchor_edges(anchor_edge: str | None, alignment: str | None):
    if not anchor_edge: anchor_edge = 'full'
    if not alignment: alignment = 'center'

    return anchor_setting_values.get(f'{anchor_edge}_{alignment}')

def set_margins(data_value: dict | None):
    if data_value:
        return Margins(
            data_value.get('top'),
            data_value.get('right'),
            data_value.get('bottom'),
            data_value.get('left')
        )
    return None

class LayerSetting:
    def __init__(self, namespace: str, layer_data: dict):
        self.namespace: str | None = namespace
        self.monitor_id: int | None = layer_data.get('monitor_id')
        self.auto_exclusive_zone: bool | None = layer_data.get('auto_exclusive_zone')
        self.exclusive_zone: int | None = layer_data.get('exclusive_zone')
        self.level: Levels | None = set_level(layer_data.get('level'))
        self.anchor_edges: List[Edges] | None = set_anchor_edges(layer_data.get('anchor_edges'), layer_data.get('alignment'))
        self.margins: Margins | None = set_margins(layer_data.get('margins'))
        self.width: int = layer_data.get('width') or -1
        self.height: int = layer_data.get('height') or -1
