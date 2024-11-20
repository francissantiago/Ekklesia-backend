from fastapi import FastAPI, HTTPException
from config.database import read_db, write_db

app = FastAPI()


# Conectar aos bancos de dados
@app.on_event("startup")
async def startup_event():
    await read_db.connect()
    await write_db.connect()


@app.on_event("shutdown")
async def shutdown():
    await read_db.disconnect()
    await write_db.disconnect()


# Rotas de exemplo
@app.get("/users")
async def get_users():
    query = "SELECT * FROM users"
    users = await read_db.fetch_all(query)
    if not users:
        raise HTTPException(status_code=404, detail="Nenhum usuário encontrado.")
    return users

