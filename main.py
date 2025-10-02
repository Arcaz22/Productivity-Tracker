import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routers.auth import router as auth_router
from app.routers.user import router as user_router
from app.routers.activity_categories import router as activity_categories_router
from app.routers.test import router as test_router

from app.core.database import engine, Base, SessionLocal
from app.utils.response.exception import (
    APIException,
    api_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PRODUCTIVITY TRACKER API", description="PRODUCTIVITY TRACKER", version="0.0.1"
)

app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, tags=["auth"])
app.include_router(user_router, tags=["user"])
app.include_router(activity_categories_router, tags=["master"])
app.include_router(test_router, tags=["test"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Productivty Tracker API",
    }
