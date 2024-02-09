from typing import Literal, TypedDict, Optional, Union

# Event Ids
ClientRuntimeEventIds = Literal['close_client']
ClientEventIds = Literal[ClientRuntimeEventIds]

# Event Data
class EventDataExampleA(TypedDict):
    data_a: str
    data_b: bool

class EventDataExampleB(TypedDict):
    data_c: str
    data_d: bool

class ClientEventObject(TypedDict):
    id: ClientEventIds
    data: Optional[Union[
        EventDataExampleA,
        EventDataExampleB
    ]]