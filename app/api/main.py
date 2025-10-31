from fastapi import APIRouter, Depends

from app.core.dependencies.service_factories import require_admin, get_current_user
import app.api.routes.client as client_routes
import app.api.routes.auth as auth_routes
import app.api.routes.admin as admin_routes

auth_router = APIRouter()
auth_router.include_router(auth_routes.google_router)

client_router = APIRouter(dependencies=[Depends(get_current_user)])
client_router.include_router(client_routes.users_router)
client_router.include_router(client_routes.categories.router)
client_router.include_router(client_routes.levels_router)
client_router.include_router(client_routes.translate_router)
client_router.include_router(client_routes.question_router)
client_router.include_router(client_routes.statistic_router)
client_router.include_router(client_routes.issues_router)
client_router.include_router(client_routes.issue_types_router)

admin_router = APIRouter(
    dependencies=[Depends(require_admin), Depends(get_current_user)]
)
#
admin_router.include_router(admin_routes.users_router)
admin_router.include_router(admin_routes.categories_router)
admin_router.include_router(admin_routes.levels_router)
admin_router.include_router(admin_routes.meanings_router)
admin_router.include_router(admin_routes.text_definitions_router)
admin_router.include_router(admin_routes.image_definitions_router)
admin_router.include_router(admin_routes.images_router)
admin_router.include_router(admin_routes.question_types_router)
admin_router.include_router(admin_routes.issues_router)
admin_router.include_router(admin_routes.issue_statuses_router)
