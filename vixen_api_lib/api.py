from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

api = FastAPI()

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

from . import hypr_endpoints
# from . import static_endpoints

HOST = '127.0.0.1'
PORT = 8420

def run():
    uvicorn.run(api, host=HOST, port=PORT)