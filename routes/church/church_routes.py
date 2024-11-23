from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from routes.auth.api_key_validate import validate_api_key
from config.database import read_db, write_db

router = APIRouter()

#########################
#### MODELOS
#########################
# Modelo base de igreja
class ChurchBase(BaseModel):
    church_name: str = Field(..., max_length=255)
    church_headquarters_id: int
    church_address: str = Field(..., max_length=255)
    church_address_number: int
    church_complement: Optional[str] = Field(None, max_length=20)
    church_district: str = Field(..., max_length=50)
    church_postal_code: str = Field(
        ..., pattern=r"^\d{8}$", description="CEP deve conter 8 números."
    )
    church_city: str = Field(..., max_length=50)
    church_state: str = Field(..., max_length=5)
    church_country: str = Field(..., max_length=400)
    church_status: Optional[int] = 1

# Modelo de criação de igreja
class ChurchCreate(ChurchBase):
    pass

# Modelo de atualização de igreja
class ChurchUpdate(BaseModel):
    church_name: Optional[str] = Field(None, max_length=255)
    church_headquarters_id: Optional[int]
    church_address: Optional[str] = Field(None, max_length=255)
    church_address_number: Optional[int]
    church_complement: Optional[str] = Field(None, max_length=20)
    church_district: Optional[str] = Field(None, max_length=50)
    church_postal_code: Optional[str] = Field(
        None, pattern=r"^\d{8}$", description="CEP deve conter 8 números."
    )
    church_city: Optional[str] = Field(None, max_length=50)
    church_state: Optional[str] = Field(None, max_length=5)
    church_country: str = Field(..., max_length=400)
    church_status: Optional[int]

#########################
#### ROTAS DE IGREJAS
#########################
# Seleciona um registro de igreja por id
@router.get("/{church_id}", dependencies=[Depends(validate_api_key)])
async def get_church_by_church_id(church_id: int):
    query = "SELECT * FROM churches WHERE church_id = %s"
    record = await read_db.fetch_one(query, [church_id])
    if not record:
        raise HTTPException(status_code=404, detail="Registro de igreja não encontrado.")
    return record

# Cria uma nova igreja
@router.post("/create_church", status_code=201, dependencies=[Depends(validate_api_key)])
async def create_church(church: ChurchCreate):
    """Cria uma nova igreja."""
    query_insert = """
    INSERT INTO churches (
        church_name, church_headquarters_id, church_address, church_address_number,
        church_complement, church_district, church_postal_code, church_city, church_state,
        church_country, church_status
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        await write_db.execute(
            query_insert,
            [
                church.church_name,
                church.church_headquarters_id,
                church.church_address,
                church.church_address_number,
                church.church_complement,
                church.church_district,
                church.church_postal_code,
                church.church_city,
                church.church_state,
                church.church_country,
                church.church_status,
            ],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao criar igreja.") from e

    return {"message": "Igreja criada com sucesso."}

# Atualiza uma igreja
@router.put("/edit_church/{church_id}", status_code=200, dependencies=[Depends(validate_api_key)])
async def update_church(church_id: int, church: ChurchUpdate):
    """Atualiza uma igreja."""
    fields = []
    values = []

    for field, value in church.model_dump(exclude_unset=True).items():
        fields.append(f"{field} = %s")
        values.append(value)

    if not fields:
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar.")

    query_update = f"""
    UPDATE churches
    SET {', '.join(fields)}, church_updated_at = CURRENT_TIMESTAMP
    WHERE church_id = %s
    """
    values.append(church_id)

    try:
        result = await write_db.execute(query_update, values)
        if result == 0:
            raise HTTPException(status_code=404, detail="Igreja não encontrada.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao atualizar igreja.") from e

    return {"message": "Igreja atualizada com sucesso."}

# Remove uma igreja
@router.delete("/delete_church/{church_id}", status_code=200, dependencies=[Depends(validate_api_key)])
async def delete_church(church_id: int):
    """Remove uma igreja."""
    query_delete = "DELETE FROM churches WHERE church_id = %s"
    try:
        result = await write_db.execute(query_delete, [church_id])
        if result == 0:
            raise HTTPException(status_code=404, detail="Igreja não encontrada.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao remover igreja.") from e

    return {"message": "Igreja removida com sucesso."}
