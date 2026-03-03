from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import app.models
from app.database import create_all_tables
from app.routers.auth_router import router as auth_router
from app.routers.course_router import router as course_router
from app.routers.student_router import router as student_router
from app.routers.cohere_router import router as cohere_router
from app.routers.cv_router import router as cv_router
from app.routers.embedding_router import router as embedding_router
from app.routers.rag_router import router as rag_router
from app.routers.video_router import router as video_router

app = FastAPI(title="Student API")


@app.on_event("startup")
def on_startup():
    create_all_tables()


app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(student_router, prefix="/students", tags=["Students"])
app.include_router(course_router, prefix="/courses", tags=["Courses"])
app.include_router(cv_router)
app.include_router(embedding_router)
app.include_router(rag_router)
app.include_router(video_router)

from app.routers import cohere_router
app.include_router(cohere_router.router)

from app.routers.storage_router import router as storage_router
app.include_router(storage_router)


@app.get("/")
def read_root():
    return {"message": "????? ??? ?? API ??????!"}