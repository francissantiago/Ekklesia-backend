from fastapi import Request, HTTPException, status
from config.database import read_db
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY_HEADER = os.getenv("FRONTEND_HEADER_FIELD")

async def validate_api_key(request: Request):
    api_key = request.headers.get(API_KEY_HEADER)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key não fornecida.",
            headers={"WWW-Authenticate": "API Key"},
        )

    # Verifica a chave no banco de dados
    query = "SELECT * FROM api_keys WHERE `key` = %s"
    result = await read_db.fetch_one(query, (api_key,))
    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key inválida.",
        )
