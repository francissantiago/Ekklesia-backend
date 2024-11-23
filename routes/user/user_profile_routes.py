from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from routes.auth.api_key_validate import validate_api_key
from config.database import read_db
from config.database import write_db

router = APIRouter()


#########################
#### MODELOS
#########################
# Modelo de criação de perfil
class UserProfileBase(BaseModel):
    user_profile_user_id: int
    user_profile_name: str = Field(..., max_length=255)
    user_profile_cpf: str = Field(
        ..., pattern=r"^\d{11}$", description="CPF deve conter 11 números."
    )
    user_profile_address: Optional[str] = Field(None, max_length=255)
    user_profile_address_number: Optional[int]
    user_profile_address_complement: Optional[str] = Field(None, max_length=30)
    user_profile_district: Optional[str] = Field(None, max_length=50)
    user_profile_postal_code: Optional[str] = Field(
        None, pattern=r"^\d{8}$", description="CEP deve conter 8 números."
    )
    user_profile_city: Optional[str] = Field(None, max_length=50)
    user_profile_state: Optional[str] = Field(None, max_length=5)
    user_profile_country: Optional[str] = Field(None, max_length=40)
    user_profile_phone_number: Optional[str] = Field(
        None,
        pattern=r"^\d{10,15}$",
        description="Número de telefone deve conter entre 10 e 15 números.",
    )
    user_profile_photo: Optional[str] = Field(None, max_length=255)


# Modelo de atualização de perfil
class UserProfileUpdate(BaseModel):
    user_profile_name: str = Field(..., max_length=255)
    user_profile_cpf: str = Field(
        ..., pattern=r"^\d{11}$", description="CPF deve conter 11 números."
    )
    user_profile_address: Optional[str] = Field(None, max_length=255)
    user_profile_address_number: Optional[int]
    user_profile_address_complement: Optional[str] = Field(None, max_length=30)
    user_profile_district: Optional[str] = Field(None, max_length=50)
    user_profile_postal_code: Optional[str] = Field(
        None, pattern=r"^\d{8}$", description="CEP deve conter 8 números."
    )
    user_profile_city: Optional[str] = Field(None, max_length=50)
    user_profile_state: Optional[str] = Field(None, max_length=5)
    user_profile_country: Optional[str] = Field(None, max_length=40)
    user_profile_phone_number: Optional[str] = Field(
        None,
        pattern=r"^\d{10,15}$",
        description="Número de telefone deve conter entre 10 e 15 números.",
    )
    user_profile_photo: Optional[str] = Field(None, max_length=255)


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileUpdate):
    pass


#########################
#### ROTAS DE PERFIL
#########################
# Seleciona um perfil por usuário
@router.get("/profile/{user_id}", dependencies=[Depends(validate_api_key)])
async def get_profile_by_user_id(user_id: int):
    query = "SELECT * FROM users_profile WHERE user_profile_user_id = %s"
    record = await read_db.fetch_one(query, [user_id])
    if not record:
        raise HTTPException(
            status_code=404, detail="Registro de perfil não encontrado."
        )
    return record


# Cria um novo perfil de usuário
@router.post("/profile/create", status_code=201, dependencies=[Depends(validate_api_key)])
async def create_profile(profile: UserProfileCreate):
    """Cria um novo perfil de usuário."""
    query_insert = """
    INSERT INTO users_profile (
        user_profile_user_id, user_profile_name, user_profile_cpf, user_profile_address, 
        user_profile_address_number, user_profile_address_complement,
        user_profile_district, user_profile_postal_code, user_profile_city,
        user_profile_state, user_profile_country, user_profile_phone_number, 
        user_profile_photo
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        await write_db.execute(
            query_insert,
            [
                profile.user_profile_user_id,
                profile.user_profile_name,
                profile.user_profile_cpf,
                profile.user_profile_address,
                profile.user_profile_address_number,
                profile.user_profile_address_complement,
                profile.user_profile_district,
                profile.user_profile_postal_code,
                profile.user_profile_city,
                profile.user_profile_state,
                profile.user_profile_country,
                profile.user_profile_phone_number,
                profile.user_profile_photo,
            ],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao criar perfil.") from e

    return {"message": "Perfil criado com sucesso."}


# Atualiza um perfil de usuário
@router.put(
    "/profile/edit/{profile_id}", status_code=200, dependencies=[Depends(validate_api_key)]
)
async def update_profile(profile_id: int, profile: UserProfileUpdate):
    """Atualiza um perfil de usuário."""
    query_update = """
    UPDATE users_profile
    SET user_profile_name = %s,
        user_profile_cpf = %s,
        user_profile_address = %s,
        user_profile_address_number = %s,
        user_profile_address_complement = %s,
        user_profile_district = %s,
        user_profile_postal_code = %s,
        user_profile_city = %s,
        user_profile_state = %s,
        user_profile_country = %s,
        user_profile_phone_number = %s,
        user_profile_photo = %s,
        user_profile_updated_at = CURRENT_TIMESTAMP
    WHERE user_profile_user_id = %s
    """
    try:
        result = await write_db.execute(
            query_update,
            [
                profile.user_profile_name,
                profile.user_profile_cpf,
                profile.user_profile_address,
                profile.user_profile_address_number,
                profile.user_profile_address_complement,
                profile.user_profile_district,
                profile.user_profile_postal_code,
                profile.user_profile_city,
                profile.user_profile_state,
                profile.user_profile_country,
                profile.user_profile_phone_number,
                profile.user_profile_photo,
                profile_id,
            ],
        )
        if result == 0:
            raise HTTPException(status_code=404, detail="Perfil não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao atualizar perfil.") from e

    return {"message": "Perfil atualizado com sucesso."}


# Remove um perfil de usuário.
@router.delete(
    "/profile/delete/{profile_id}", status_code=200, dependencies=[Depends(validate_api_key)]
)
async def delete_profile(profile_id: int):
    """Remove um perfil de usuário."""
    query_delete = "DELETE FROM users_profile WHERE user_profile_user_id = %s"
    try:
        result = await write_db.execute(query_delete, [profile_id])
        if result == 0:
            raise HTTPException(status_code=404, detail="Perfil não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao remover perfil.") from e

    return {"message": "Perfil removido com sucesso."}
