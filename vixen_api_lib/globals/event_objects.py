from typing import Dict, TypedDict, Optional

class EventObject(TypedDict):
    id: str
    data: Optional[Dict]

class EventData(TypedDict):
    pass