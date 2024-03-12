import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173"
]


from .globals import DevMode, get_front_url
from .features import Features

@asynccontextmanager
async def lifespan(api: FastAPI):
    yield
    await Features.cleanup()

api = FastAPI(lifespan=lifespan)

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = uvicorn.Config(api, host='localhost', port=6481)
server = uvicorn.Server(config)

@api.get('/ping')
async def ping():
    return {'is_online': True}

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
    
# from . import static_endpoints