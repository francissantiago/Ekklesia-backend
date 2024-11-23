from fastapi import APIRouter, Depends, HTTPException
from routes.auth.api_key_validate import validate_api_key
from config.database import read_db, write_db

router = APIRouter()

#########################
#### ROTAS DE 2FA
#########################
# Seleciona todos os registros 2FA
@router.get("/2fa/list_all_2fa", dependencies=[Depends(validate_api_key)])
async def get_all_2fa():
    query = "SELECT * FROM users_2fa"
    records = await read_db.fetch_all(query)
    if not records:
        raise HTTPException(status_code=404, detail="Nenhum registro encontrado.")
    return records
