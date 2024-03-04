from fastapi import WebSocket
from .FeaturePipe import ClientEvent
from .parameters import FeatureParams

class FeatureState:
    def __init__(self, feature_params: FeatureParams):
        self.feature_params = feature_params
        self.state = self.feature_params.state or {}

    def save_state(self):
        self.feature_params.state = self.state
        self.feature_params.save()

    async def handle_get_state_event(self, client_websocket: WebSocket):
        await client_websocket.send_json(ClientEvent(
            id = 'GET_STATE',
            data = {'state': self.state}
        ))

    async def handle_set_state_event(self, state: dict | None, dispatcher):
        if state:
            self.state.update(state)

            await dispatcher(ClientEvent(
                id = 'UPDATE_STATE',
                data = {'state': self.state}
            ))