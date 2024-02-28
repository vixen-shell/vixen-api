import json
from functools import wraps
from fastapi import WebSocket
from typing import Dict, Literal, TypedDict, Optional, Any

class EventDataState(TypedDict):
    state: Dict[str, str | int | bool]

class EventObject(TypedDict):
    id: str
    data: Optional[Any]

class PipeEvent(EventObject):
    id: Literal['GET_STATE', 'SET_STATE', 'SAVE_STATE', 'CLOSE_PIPE']
    data: Optional[
        EventDataState
    ]

class ClientEvent(EventObject):
    id: Literal['UPDATE_STATE']
    data: Optional[
        EventDataState
    ]

class FeaturePipe:
    def __init__(self, initial_state: Dict | None, setting_file_path: str):
        self.is_open = False
        self.setting_file_path = setting_file_path
        self.client_websocket: Dict[str, WebSocket] = {}
        self.feature_state = initial_state or {}

    def open_pipe(self):
        if not self.is_open:
            self.is_open = True

    async def close_pipe(self, reason: str):
        if self.is_open:
            self.is_open = False

            ids = list(self.client_websocket.keys())
            for id in ids:
                await self.client_websocket[id].close(
                    code = 1000,
                    reason = reason
                )

            self.client_websocket = {}

    async def connect_client(self, client_id: str, client_websocket: WebSocket):
        if self.is_open:
            if not client_id in self.client_websocket:
                await client_websocket.accept()
                self.client_websocket[client_id] = client_websocket

    def remove_client(self, client_id: str):
        if self.is_open:
            if client_id in self.client_websocket:
                del self.client_websocket[client_id]

    async def dispatch_event(self, client_id, event: EventObject):
        if self.is_open:
            for id in self.client_websocket:
                if not id == client_id:
                    client_websocket = self.client_websocket[id]
                    await client_websocket.send_json(event)

    async def handle_state_event(self, client_id: str, event: PipeEvent):
        if self.is_open:
            if event['id'] == 'GET_STATE':
                await self.client_websocket[client_id].send_json(
                    ClientEvent(
                        id = 'UPDATE_STATE',
                        data = {'state': self.feature_state}
                    )
                )

            if event['id'] == 'SET_STATE':
                if 'data' in event:
                    if 'state' in event['data']:
                        self.feature_state.update(event['data']['state'])

                await self.dispatch_event(client_id, ClientEvent(
                    id = 'UPDATE_STATE',
                    data = {'state': self.feature_state}
                ))

    def save_state(self):
        if self.is_open:
            with open(self.setting_file_path, 'r') as file:
                setting_data: dict = json.load(file)

            setting_data['state'] = self.feature_state

            with open(self.setting_file_path, 'w') as file:
                json.dump(setting_data, file, indent = 4)

    async def handle_event(self, event: PipeEvent):
        if self.is_open:
            await self.handle_state_event(self.client_id, event)
            if event['id'] == 'SAVE_STATE': self.save_state()

            # await feature.pipe.broadcast_data(websocket, feature_name, data)