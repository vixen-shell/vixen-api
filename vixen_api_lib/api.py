import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .clients import start_default_clients

@asynccontextmanager
async def lifespan(api: FastAPI):
    start_default_clients()
    yield

api = FastAPI(lifespan=lifespan)
config = uvicorn.Config(api, host='localhost', port=6481)
server = uvicorn.Server(config)

from . import hypr_endpoints
from . import clients_endpoints

def run():
    server.run()

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