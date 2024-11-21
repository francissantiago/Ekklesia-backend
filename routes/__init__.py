from fastapi import APIRouter

# Rotas de chaves de API
from .auth.api_key_routes import router as api_key_routes

# Rotas de Usuário
from .users.users_routes import router as users_router

# Rotas de Usuário
from .users.profile_routes import router as profile_routes

router = APIRouter()

# Rotas de chaves de API
router.include_router(api_key_routes, prefix="/auth", tags=["api_auth"])

# Rotas de Usuário
router.include_router(users_router, prefix="/users", tags=["users"])

# Rotas de Perfil de Usuário
router.include_router(profile_routes, prefix="/user_profiles", tags=["user_profiles"])

__all__ = ["router"]
