from contextlib import asynccontextmanager

from app.api import auth, chat, metrics
from app.db.database import database
from app.middleware.auth_middleware import AuthMiddleware
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.rate_limit_middleware import RateLimitMiddleware
from fastapi import FastAPI

# define what we do when the app starts and shuts down: start and stop the database connection gracefully
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await database.connect()
    yield
    # Shutdown logic
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

# Include routers from different modules. routers are our endpoints. they are defined in the api module
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(metrics.router)

# Apply middlewares
app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuthMiddleware)
app.add_middleware(LoggingMiddleware)
