import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.database import write_db

router = APIRouter()

# Define o modelo para o corpo da requisição
class APIKeyRequest(BaseModel):
    description: str

@router.post("/generate-api-key")
async def generate_api_key(request: APIKeyRequest):
    # Gera uma chave única
    api_key = str(uuid.uuid4())
    
    # Salva a chave no banco de dados
    query = "INSERT INTO api_keys (`key`, description) VALUES (%s, %s)"
    try:
        await write_db.execute(query, (api_key, request.description))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao gerar API Key.")

    return {"api_key": api_key}
