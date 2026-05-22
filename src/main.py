import sys
from contextlib import asynccontextmanager

import redis.asyncio as aioredis
import uvicorn

from pathlib import Path

from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache

sys.path.append(str(Path(__file__).parent.parent))
from fastapi import FastAPI
from src.api.auth import router as auth_router
from src.api.orders import router as order_router
from src.api.responses import router as response_router
from src.api.profiles import router as profile_router
from src.api.reviews import router as review_router
from src.api.admins import router as admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(order_router)
app.include_router(response_router)
app.include_router(profile_router)
app.include_router(review_router)
app.include_router(admin_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
