from fastapi import FastAPI
from loguru import logger

app = FastAPI()


@app.on_event("startup")
def on_startup():
    logger.info("startup complete")


@app.get("/")
def read_root():
    logger.info("handling root request")
    return {"message": "hello from loguru + uvicorn"}


@app.get("/health")
def health_check():
    logger.info("health check requested")
    return {"status": "ok"}
