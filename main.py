from fastapi import FastAPI
import asyncio
from config.database import read_db, write_db
from routes import router as api_router

async def app_lifespan(app: FastAPI):
    await read_db.connect()
    await write_db.connect()
    yield
    try:
        if read_db.pool is not None:
            await asyncio.wait_for(read_db.disconnect(), timeout=5)
        if write_db.pool is not None:
            await asyncio.wait_for(write_db.disconnect(), timeout=5)
    except asyncio.TimeoutError:
        print("Aviso: Encerramento de conexão demorou mais do que o esperado.")

app = FastAPI(lifespan=app_lifespan)

# Inclui as rotas do módulo users
app.include_router(api_router, prefix="/api")
