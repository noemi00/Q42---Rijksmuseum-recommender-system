from fastapi import FastAPI

from dotenv import load_dotenv
from app.routers import painting_router, user_router, token_router, evaluation_router

import os

load_dotenv()

app = FastAPI()

app.include_router(painting_router.painting_router)
app.include_router(user_router.user_router)
app.include_router(token_router.token_router)
app.include_router(evaluation_router.evaluation_router)

# Enable CORS for development
print("DEBUG=", str(os.getenv("DEBUG")))

if os.getenv("DEBUG"):
    from fastapi.middleware.cors import CORSMiddleware

    origins = [
        "http://localhost:3000",
        "http://localhost:5000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
