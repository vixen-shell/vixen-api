from typing import TypedDict, Optional, Any, Literal

class EventObject(TypedDict):
    id: str
    data: Optional[Any]

class EventData:
    class StateItem(TypedDict):
        key: str
        value: None | str | int | float | bool

    class Log(TypedDict):
        level: Optional[Literal['INFO', 'WARNING', 'ERROR']]
        message: str

class InputEvent(EventObject):
    id: Literal[
        'GET_STATE',
        'SET_STATE',
        'SAVE_STATE',
        'LOG'
    ]
    data: Optional[
        EventData.StateItem |
        EventData.Log
    ]

class OutputEvent(EventObject):
    id: Literal[
        'UPDATE_STATE',
        'LOG'
    ]
    data: Optional[
        EventData.StateItem |
        EventData.Log
    ]