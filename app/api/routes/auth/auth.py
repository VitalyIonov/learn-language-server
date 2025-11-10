from fastapi import APIRouter
from starlette.responses import JSONResponse

router = APIRouter(tags=["auth"])


@router.post("/logout")
async def logout():
    resp = JSONResponse({"ok": True})
    resp.delete_cookie(
        key="access_token",
        path="/",
        samesite="lax",
    )

    return resp
