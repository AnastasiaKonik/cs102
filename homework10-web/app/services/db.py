import traceback

from fastapi.logger import logger
from tortoise import Tortoise
from tortoise.backends.base.config_generator import generate_config

from app import app
from app.services import settings

tortoise_config: dict = generate_config(settings.POSTGRES_URI, {"models": ["app.models"]})


def describe_credentials():
    described_models: dict = tortoise_config
    for database in described_models.get("connections"):
        source_pass = settings.POSTGRES_PASSWORD
        if len(source_pass) > 0:
            hided_pass = source_pass[0] + "*" * len(source_pass[1:-1]) + source_pass[-1]
            described_models["connections"][database]["credentials"]["password"] = hided_pass

    return described_models


@app.on_event("startup")
async def on_startup():
    try:
        await Tortoise.init(
            config=tortoise_config,
        )
        await Tortoise.generate_schemas()
        logger.info("PostgreSQL Connection opened")
        logger.info(describe_credentials())
    except Exception as e:
        traceback.print_exc()


@app.on_event("shutdown")
async def on_shutdown():
    await Tortoise.close_connections()
