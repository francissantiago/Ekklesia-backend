import uuid
from fastapi import APIRouter, HTTPException
from config.database import write_db

router = APIRouter()

@router.post("/generate-api-key")
async def generate_api_key(description: str):
    # Gera uma chave única
    api_key = str(uuid.uuid4())
    
    # Salva a chave no banco de dados
    query = "INSERT INTO api_keys (`key`, description) VALUES (%s, %s)"
    try:
        await write_db.execute(query, (api_key, description))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao gerar API Key.")

    return {"api_key": api_key}
