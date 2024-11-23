from fastapi import APIRouter, Depends, HTTPException
from routes.auth.api_key_validate import validate_api_key
from config.database import read_db
from config.database import write_db

router = APIRouter()
#########################
#### ROTAS DE PERFIL
#########################
# Seleciona todos os perfis
@router.get("/profiles/list_all", dependencies=[Depends(validate_api_key)])
async def get_profiles():
    query = "SELECT * FROM users_profile"
    users = await read_db.fetch_all(query)
    if not users:
        raise HTTPException(status_code=404, detail="Nenhum perfil encontrado.")
    return users