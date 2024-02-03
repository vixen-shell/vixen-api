import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .features import start_active_features

@asynccontextmanager
async def lifespan(api: FastAPI):
    start_active_features()
    yield

api = FastAPI(lifespan=lifespan)

from . import hypr_endpoints
from . import features_endpoints

HOST = 'localhost'
PORT = 6481

def run():
    uvicorn.run(api, host=HOST, port=PORT)

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