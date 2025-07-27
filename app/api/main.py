from fastapi import APIRouter, Depends

from app.api.routes import login, users, categories, levels, meanings, definitions
from app.core.dependencies import require_admin, get_current_user

api_router = APIRouter()

admin_router = APIRouter(
    prefix="/admin", dependencies=[Depends(require_admin), Depends(get_current_user)]
)
#
admin_router.include_router(users.router)
admin_router.include_router(categories.router)
admin_router.include_router(levels.router)
admin_router.include_router(meanings.router)
admin_router.include_router(definitions.router)

api_router.include_router(login.router)
api_router.include_router(admin_router)
