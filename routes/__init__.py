from fastapi import APIRouter

############################
#### SECURITY IMPORTS
############################
from .auth.api_key_routes import router as api_key_routes # Rotas de chaves de API

############################
#### ADMIN IMPORTS
############################
#Users
from .admin.users.user_permissions_routes import router as admin_users_permissions_routes # Rotas Administrativas de Permissões Usuários
from .admin.users.users_2fa_routes import router as admin_users_2fa_routes # Rotas Administrativas de Autenticação de 2 Fatores de Usuários
from .admin.users.users_profile_routes import router as admin_users_profile_routes # Rotas Administrativas de Perfis de Usuários
from .admin.users.users_routes import router as admin_users_router # Rotas Administrativas de Usuários
# Churches
from .admin.churches.churches_routes import router as admin_churches_routes # Rotas Administrativas de Igrejas

############################
#### USER IMPORTS
############################
# User
from .user.user_2fa_routes import router as users_2fa_routes # Rotas de 2FA
from .user.user_routes import router as user_router # Rotas de Usuário
from .user.user_profile_routes import router as users_profile_routes # Rotas de Perfil Usuário
# Church
from .church.church_routes import router as church_routes # Rotas de Igreja

router = APIRouter()

############################
#### ROTAS DE SEGURANÇA
############################
router.include_router(api_key_routes, prefix="/auth", tags=["api_auth"])

############################
#### ROTAS ADMINISTRATIVAS
############################
# Igrejas
router.include_router(admin_churches_routes, prefix="/admin/churches", tags=["admin_churches"])

# Usuários
router.include_router(admin_users_permissions_routes, prefix="/admin/users", tags=["admin_users_permissions"])
router.include_router(admin_users_2fa_routes, prefix="/admin/users", tags=["admin_users_2fa"])
router.include_router(admin_users_profile_routes, prefix="/admin/users", tags=["admin_users_profiles"])
router.include_router(admin_users_router, prefix="/admin/users", tags=["admin_users"])

############################
#### ROTAS DE USUÁRIO
############################
# Igreja
router.include_router(church_routes, prefix="/church", tags=["church"])

# Usuário
router.include_router(users_2fa_routes, prefix="/user", tags=["user_2fa"])
router.include_router(users_profile_routes, prefix="/user", tags=["user_profile"])
router.include_router(user_router, prefix="/user", tags=["user"])

__all__ = ["router"]
