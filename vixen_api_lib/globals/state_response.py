from fastapi import Response
from pydantic import BaseModel

class State_Response:
    def __init__(self, response: Response, status_code: int):
        self.status_code = status_code
        self.response = response
    
    def __call__(self, model: BaseModel) -> BaseModel:
        self.response.status_code = self.status_code
        return model