from fastapi import APIRouter

from .auth.api_key_routes import router as api_key_routes # Rotas de chaves de API
from .users.users_routes import router as users_router # Rotas de Usuário
from .users.users_profile_routes import router as users_profile_routes # Rotas de Perfil Usuário
from .users.users_2fa_routes import router as users_2fa_routes # Rotas de 2FA
from .churchs.churchs_routs import router as churchs_routs # Rotas de Igrejas

router = APIRouter()

# Rotas de chaves de API
router.include_router(api_key_routes, prefix="/auth", tags=["api_auth"])

# Rotas de Usuário
router.include_router(users_router, prefix="/users", tags=["users"])

# Rotas de Perfil de Usuário
router.include_router(users_profile_routes, prefix="/user_profiles", tags=["user_profiles"])

# Rotas de 2FA
router.include_router(users_2fa_routes, prefix="/user_2fa", tags=["user_2fa"])

# Rotas de 2FA
router.include_router(churchs_routs, prefix="/churchs", tags=["churchs"])

__all__ = ["router"]
