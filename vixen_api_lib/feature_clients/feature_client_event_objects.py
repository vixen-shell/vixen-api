from typing import Literal, Optional, Union
from ..event_objects import EventObject, EventData

# Event Ids
FeatureClientRuntimeEventIds = Literal['close_client']
FeatureClientEventIds = Literal[FeatureClientRuntimeEventIds]

# Event Data
class EventDataExampleA(EventData):
    data_a: str
    data_b: bool

class EventDataExampleB(EventData):
    data_c: str
    data_d: bool

class FeatureClientEventObject(EventObject):
    id: FeatureClientEventIds
    data: Optional[Union[
        EventDataExampleA,
        EventDataExampleB
    ]]