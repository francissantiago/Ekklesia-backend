from fastapi import APIRouter, Depends, HTTPException
from routes.auth.api_key_validate import validate_api_key
from config.database import read_db

router = APIRouter()

@router.get("/users", dependencies=[Depends(validate_api_key)])
async def get_users():
    query = "SELECT * FROM users"
    users = await read_db.fetch_all(query)
    if not users:
        raise HTTPException(status_code=404, detail="Nenhum usuário encontrado.")
    return users
