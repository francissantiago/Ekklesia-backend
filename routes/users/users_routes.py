from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from routes.auth.api_key_validate import validate_api_key
from config.database import read_db
from config.database import write_db

router = APIRouter()

@router.get("/users", dependencies=[Depends(validate_api_key)])
#########################
#### SELECIONA TODOS OS USUÁRIOS
#########################
async def get_users():
    query = "SELECT * FROM users_auth"
    users = await read_db.fetch_all(query)
    if not users:
        raise HTTPException(status_code=404, detail="Nenhum usuário encontrado.")
    return users

#########################
#### CRIA UM NOVO USUÁRIO
#########################
# Contexto de criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Modelo de entrada para validação
class UserCreate(BaseModel):
    user_email: EmailStr
    user_password: str = Field(..., min_length=8, max_length=128)

# Função para hash de senha
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Rota para criar um novo usuário
@router.post("/create_user", status_code=201)
async def create_user(user: UserCreate):
    # Hash da senha
    hashed_password = hash_password(user.user_password)

    # Verificar se o e-mail já existe
    query_check_email = "SELECT COUNT(*) as count FROM users_auth WHERE user_email = %s"
    result = await write_db.fetch_one(query_check_email, [user.user_email])
    if result["count"] > 0:
        raise HTTPException(status_code=400, detail="E-mail já registrado.")

    # Inserir novo usuário no banco
    query_insert = """
    INSERT INTO users_auth (user_email, user_password, user_permission_id, user_status)
    VALUES (%s, %s, %s, %s)
    """
    try:
        await write_db.execute(query_insert, [user.user_email, hashed_password, 12, 1])
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao criar usuário.") from e

    return {"message": "Usuário criado com sucesso."}