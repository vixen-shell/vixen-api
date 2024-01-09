from fastapi import FastAPI
import uvicorn

api = FastAPI()

from . import hypr_endpoints

HOST = '127.0.0.1'
PORT = 8420

def run():
    uvicorn.run(api, host=HOST, port=PORT)