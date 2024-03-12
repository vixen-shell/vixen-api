from typing import TypedDict, Optional, Any, Literal

class EventObject(TypedDict):
    id: str
    data: Optional[Any]

class EventData:
    class StateItem(TypedDict):
        key: str
        value: None | str | int | float | bool

class InputEvent(EventObject):
    id: Literal[
        'GET_STATE',
        'SET_STATE',
        'SAVE_STATE',
    ]
    data: Optional[
        EventData.StateItem
    ]

class OutputEvent(EventObject):
    id: Literal[
        'UPDATE_STATE'
    ]
    data: Optional[
        EventData.StateItem
    ]