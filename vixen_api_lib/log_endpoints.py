from fastapi import Response, Body
from typing import Literal
from .api import api
from .globals import ModelResponses, Models
from .log import Logger

# GET LOGS
logs_responses = ModelResponses({
    200: Models.Log.Logs
})

@api.get(
    '/logs',
    description = 'Get logs',
    responses = logs_responses.responses
)
async def get_logs(response: Response):
    return logs_responses(response, 200)(
        logs = Logger.log_cache
    )

log_responses = ModelResponses({
    200: Models.Log.Log
})

@api.post(
    '/log',
    description = 'Post a log',
    responses = log_responses.responses
)
async def post_log(
    response: Response,
    level: Literal['INFO', 'WARNING', 'ERROR'] = Body(description = "Log's level"),
    message: str = Body(description = "Log's message")
):
    Logger.log(level, message)

    return log_responses(response, 200)(
        level = level,
        message = message
    )