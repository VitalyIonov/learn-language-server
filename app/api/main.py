from fastapi import APIRouter, Depends

from app.core.dependencies.common import require_admin, get_current_user
import app.api.routes.client as client_routes
import app.api.routes.auth as auth_routes
import app.api.routes.admin as admin_routes

auth_router = APIRouter()
auth_router.include_router(auth_routes.google.router)

client_router = APIRouter(dependencies=[Depends(get_current_user)])
client_router.include_router(client_routes.users.router)
client_router.include_router(client_routes.categories.router)
client_router.include_router(client_routes.translate.router)

admin_router = APIRouter(
    dependencies=[Depends(require_admin), Depends(get_current_user)]
)
#
admin_router.include_router(admin_routes.users.router)
admin_router.include_router(admin_routes.categories.router)
admin_router.include_router(admin_routes.levels.router)
admin_router.include_router(admin_routes.meanings.router)
admin_router.include_router(admin_routes.definitions.router)
