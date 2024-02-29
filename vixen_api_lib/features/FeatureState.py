from fastapi import WebSocket
from .FeaturePipe import ClientEvent
from ..globals import SettingFile

class FeatureState:
    def __init__(self, setting_file: SettingFile):
        self.setting_file = setting_file
        self.state = setting_file.data.get('state') or {}

    def save_state(self):
        self.setting_file.data['state'] = self.state
        self.setting_file.save()

    async def handle_get_state_event(self, client_websocket: WebSocket):
        await client_websocket.send_json(ClientEvent(
            id = 'GET_STATE',
            data = {'state': self.state}
        ))

    async def handle_set_state_event(self, state: dict | None, dispatcher):
        if state:
            self.state.update(state)
            print(self.state)

            await dispatcher(ClientEvent(
                id = 'UPDATE_STATE',
                data = {'state': self.state}
            ))