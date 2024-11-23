from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from routes.auth.api_key_validate import validate_api_key
from config.database import read_db, write_db

router = APIRouter()

#########################
#### MODELOS
#########################
# Modelo base para permissões de usuário
class UserPermissionBase(BaseModel):
    user_permissions_name: str = Field(..., max_length=50)
    user_permissions_lvl: int
    user_permissions_created_by_id: int

# Modelo para criação de permissões
class UserPermissionCreate(UserPermissionBase):
    pass

# Modelo para atualização de permissões
class UserPermissionUpdate(BaseModel):
    user_permissions_name: Optional[str] = Field(None, max_length=50)
    user_permissions_lvl: Optional[int]
    user_permissions_updated_by_id: int

#########################
#### ROTAS DE PERMISSÕES
#########################
# Obter todas as permissões
@router.get("/list_all", dependencies=[Depends(validate_api_key)])
async def get_permissions():
    """Obtém todas as permissões de usuários."""
    query = "SELECT * FROM users_permissions"
    permissions = await read_db.fetch_all(query)
    if not permissions:
        raise HTTPException(status_code=404, detail="Nenhuma permissão encontrada.")
    return permissions

# Criar uma nova permissão
@router.post("/create", status_code=201, dependencies=[Depends(validate_api_key)])
async def create_permission(permission: UserPermissionCreate):
    """Cria uma nova permissão de usuário."""
    query_insert = """
    INSERT INTO users_permissions (
        user_permissions_name, user_permissions_lvl, user_permissions_created_by_id
    ) VALUES (%s, %s, %s)
    """
    try:
        await write_db.execute(
            query_insert,
            [
                permission.user_permissions_name,
                permission.user_permissions_lvl,
                permission.user_permissions_created_by_id,
            ],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao criar permissão.") from e

    return {"message": "Permissão criada com sucesso."}

# Atualizar uma permissão existente
@router.put("/edit/{permission_id}", dependencies=[Depends(validate_api_key)])
async def update_permission(permission_id: int, permission: UserPermissionUpdate):
    """Atualiza uma permissão de usuário."""
    updates = []
    values = []

    if permission.user_permissions_name is not None:
        updates.append("user_permissions_name = %s")
        values.append(permission.user_permissions_name)
    if permission.user_permissions_lvl is not None:
        updates.append("user_permissions_lvl = %s")
        values.append(permission.user_permissions_lvl)
    if permission.user_permissions_updated_by_id is not None:
        updates.append("user_permissions_updated_by_id = %s")
        values.append(permission.user_permissions_updated_by_id)

    if not updates:
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar.")

    values.append(permission_id)
    query_update = f"""
    UPDATE users_permissions
    SET {", ".join(updates)}, user_permissions_update_at = CURRENT_TIMESTAMP
    WHERE user_permissions_id = %s
    """
    try:
        result = await write_db.execute(query_update, values)
        if result == 0:
            raise HTTPException(status_code=404, detail="Permissão não encontrada.")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Erro ao atualizar permissão."
        ) from e

    return {"message": "Permissão atualizada com sucesso."}

# Remover uma permissão
@router.delete("/delete/{permission_id}", dependencies=[Depends(validate_api_key)])
async def delete_permission(permission_id: int):
    """Remove uma permissão de usuário."""
    query_delete = "DELETE FROM users_permissions WHERE user_permissions_id = %s"
    try:
        result = await write_db.execute(query_delete, [permission_id])
        if result == 0:
            raise HTTPException(status_code=404, detail="Permissão não encontrada.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao remover permissão.") from e

    return {"message": "Permissão removida com sucesso."}
