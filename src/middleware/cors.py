from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

origins = [
    'http://localhost',
    'http://localhost:8080',
]


def add_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
