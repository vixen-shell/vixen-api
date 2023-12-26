from .api import api

@api.get("/hello/{name}")
async def hello(name: str):
    return {"hello": name}