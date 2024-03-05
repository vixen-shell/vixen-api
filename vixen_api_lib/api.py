import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from .globals import DevMode, get_front_url
from .features import Features

@asynccontextmanager
async def lifespan(api: FastAPI):
    yield
    await Features.cleanup()

api = FastAPI(lifespan=lifespan)
config = uvicorn.Config(api, host='localhost', port=6481)
server = uvicorn.Server(config)

# ENDPOINTS
from . import features_endpoints
from . import frames_endpoints

# WEBSOCKETS
from . import features_websockets
from . import hypr_websockets

def run(dev_mode: bool = False):
    if dev_mode:
        DevMode.set(True)
        print(f'DEV:      Front URL: {get_front_url()}')
    if Features.init(): server.run()

# from fastapi.middleware.cors import CORSMiddleware

# origins = [
#     "http://localhost:4173"
# ]

# api.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
    
# from . import static_endpoints