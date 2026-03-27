import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import chiba, health, posts

app = FastAPI(title="API")

origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(posts.router)
app.include_router(chiba.router)
