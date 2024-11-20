from fastapi import FastAPI, HTTPException
import asyncio
from config.database import read_db, write_db

# Configuração do ciclo de vida com lifespan
async def app_lifespan(app: FastAPI):
    # Conectar aos bancos de dados no início
    await read_db.connect()
    await write_db.connect()
    yield  # Espera até que o aplicativo seja encerrado
    # Desconectar bancos de dados no fim
    try:
        if read_db.pool is not None:
            await asyncio.wait_for(read_db.disconnect(), timeout=5)
        if write_db.pool is not None:
            await asyncio.wait_for(write_db.disconnect(), timeout=5)
    except asyncio.TimeoutError:
        print("Aviso: Encerramento de conexão demorou mais do que o esperado.")

# Criar a instância do FastAPI
app = FastAPI(lifespan=app_lifespan)

# Rotas de exemplo
@app.get("/users")
async def get_users():
    query = "SELECT * FROM users"
    users = await read_db.fetch_all(query)
    if not users:
        raise HTTPException(status_code=404, detail="Nenhum usuário encontrado.")
    return users
