from fastapi import FastAPI
from uvicorn import run
api = FastAPI()

from . import endpoints_test

def run_vixen_api():
    run(api, host="127.0.0.1", port=8420)