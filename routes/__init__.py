from fastapi import APIRouter

# Rotas de chaves de API
from .auth.api_key_routes import router as api_key_routes

# Rotas de Usuário
from .users.users_routes import router as users_router

router = APIRouter()

# Rotas de chaves de API
router.include_router(api_key_routes, prefix="/auth", tags=["generate_api_key"])

# Rotas de Usuário
router.include_router(users_router, prefix="/users", tags=["users"])

__all__ = ["router"]
