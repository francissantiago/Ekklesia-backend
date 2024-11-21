from fastapi import FastAPI
import asyncio
import signal
from config.database import read_db, write_db
from routes import router as api_router

# Função para desconexão forçada
async def force_disconnect():
    try:
        # Definir timeout para desconexão do read_db
        if read_db.pool is not None:
            await asyncio.wait_for(read_db.disconnect(), timeout=5)
        # Definir timeout para desconexão do write_db
        if write_db.pool is not None:
            await asyncio.wait_for(write_db.disconnect(), timeout=5)
    except asyncio.TimeoutError:
        print("Aviso: Desconexão do banco de dados demorou mais do que o esperado.")

# Captura o sinal de interrupção para encerramento imediato
def handle_shutdown_signal():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(force_disconnect())
    loop.stop()
    print("Conexões encerradas imediatamente.")

# Configuração do app FastAPI com lifespan
async def app_lifespan(app: FastAPI):
    await read_db.connect()
    await write_db.connect()
    yield
    await force_disconnect()

app = FastAPI(lifespan=app_lifespan)

# Inclui as rotas do módulo users
app.include_router(api_router, prefix="/api")

# Configura o sinal SIGINT para encerramento imediato
signal.signal(signal.SIGINT, lambda sig, frame: handle_shutdown_signal())
