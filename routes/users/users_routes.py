from fastapi import APIRouter, HTTPException
from config.database import read_db

router = APIRouter()

@router.get("/users")
async def get_users():
    query = "SELECT * FROM users"
    users = await read_db.fetch_all(query)
    if not users:
        raise HTTPException(status_code=404, detail="Nenhum usuário encontrado.")
    return users
