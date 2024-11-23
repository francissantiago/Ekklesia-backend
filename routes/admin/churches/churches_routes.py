from fastapi import APIRouter, Depends, HTTPException
from routes.auth.api_key_validate import validate_api_key
from config.database import read_db, write_db

router = APIRouter()
#########################
#### ROTAS DE IGREJAS
#########################
# Seleciona todas as igrejas
@router.get("/list_all", dependencies=[Depends(validate_api_key)])
async def get_churches():
    query = "SELECT * FROM churches"
    churches = await read_db.fetch_all(query)
    if not churches:
        raise HTTPException(status_code=404, detail="Nenhuma igreja encontrada.")
    return churches