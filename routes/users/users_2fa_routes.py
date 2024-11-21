from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from routes.auth.api_key_validate import validate_api_key
from config.database import read_db, write_db

router = APIRouter()

#########################
#### MODELOS
#########################
class TwoFactorAuthBase(BaseModel):
    user_2fa_user_id: int
    user_2fa_enabled: str = Field(..., pattern="^(Y|N)$")
    user_2fa_recovery_code: Optional[str] = Field(None, max_length=255)

class TwoFactorAuthUpdate(BaseModel):
    user_2fa_enabled: str = Field(..., pattern="^(Y|N)$")
    user_2fa_recovery_code: Optional[str] = Field(None, max_length=255)

#########################
#### ROTAS DE 2FA
#########################
# Seleciona todos os registros 2FA
@router.get("/2fa", dependencies=[Depends(validate_api_key)])
async def get_all_2fa():
    query = "SELECT * FROM users_2fa"
    records = await read_db.fetch_all(query)
    if not records:
        raise HTTPException(status_code=404, detail="Nenhum registro encontrado.")
    return records

# Seleciona um registro de 2FA por usuário
@router.get("/2fa/user/{user_id}", dependencies=[Depends(validate_api_key)])
async def get_2fa_by_user_id(user_id: int):
    query = "SELECT * FROM users_2fa WHERE user_2fa_user_id = %s"
    record = await read_db.fetch_one(query, [user_id])
    if not record:
        raise HTTPException(status_code=404, detail="Registro de 2FA não encontrado.")
    return record

# Cria um registro de 2FA
@router.post("/2fa/create_2fa", status_code=201, dependencies=[Depends(validate_api_key)])
async def create_2fa(data: TwoFactorAuthBase):
    query_insert = """
    INSERT INTO users_2fa (user_2fa_user_id, user_2fa_enabled, user_2fa_recovery_code)
    VALUES (%s, %s, %s)
    """
    try:
        await write_db.execute(
            query_insert,
            [data.user_2fa_user_id, data.user_2fa_enabled, data.user_2fa_recovery_code],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao criar registro de 2FA.") from e

    return {"message": "Registro de 2FA criado com sucesso."}

# Atualiza um registro de 2FA
@router.put("/2fa/update_2fa/user/{user_id}", status_code=200, dependencies=[Depends(validate_api_key)])
async def update_2fa(user_id: int, data: TwoFactorAuthUpdate):
    query_update = """
    UPDATE users_2fa
    SET user_2fa_enabled = %s,
        user_2fa_recovery_code = %s,
        user_2fa_updated_at = CURRENT_TIMESTAMP
    WHERE user_2fa_user_id = %s
    """
    try:
        result = await write_db.execute(
            query_update, [data.user_2fa_enabled, data.user_2fa_recovery_code, user_id]
        )
        if result == 0:
            raise HTTPException(status_code=404, detail="Registro de 2FA não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao atualizar registro de 2FA.") from e

    return {"message": "Registro de 2FA atualizado com sucesso."}

# Remove um registro de 2FA
@router.delete("/2fa/delete_2fa/user/{user_id}", status_code=200, dependencies=[Depends(validate_api_key)])
async def delete_2fa(user_id: int):
    query_delete = "DELETE FROM users_2fa WHERE user_2fa_user_id = %s"
    try:
        result = await write_db.execute(query_delete, [user_id])
        if result == 0:
            raise HTTPException(status_code=404, detail="Registro de 2FA não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao remover registro de 2FA.") from e

    return {"message": "Registro de 2FA removido com sucesso."}
