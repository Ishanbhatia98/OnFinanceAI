import typing

import typing_extensions

typing.Literal = typing_extensions.Literal

import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

import config
from router.conversation import router as conversation_router
from core.query_job import query_job_queue

import threading

threading.Thread(target=query_job_queue.run_on_loop)


app = FastAPI(
    title="OpenFinance AI",
    description="",
    version="1.0",
    docs_url="/jarvis/swagger",
    openapi_url="/jarvis/openapi.json",
    redoc_url="/jarvis/documentation",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/jarvis/health", tags=["HEALTH"])
async def health_check():
    return {"status": "ok"}


app.include_router(conversation_router, prefix='/jarvis')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    logger.info(f"Running on port : {port}")
    logger.info("Registered Routers: ")
    for route in app.routes:
        logger.info((route.name, route.path))
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            log_level="debug",
            port=5002,
            debug=True,
        )
    except:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            log_level="debug",
            port=5003,
            # debug=True,
        )
