from fastapi import APIRouter

# Rotas de Usuário
from .users.users_routes import router as users_router

router = APIRouter()

# Rotas de Usuário
router.include_router(users_router, prefix="/users", tags=["users"])

__all__ = ["router"]
