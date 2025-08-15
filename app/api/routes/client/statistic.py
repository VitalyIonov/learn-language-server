from fastapi import APIRouter, Depends

from app.core.dependencies.common import get_current_user, get_statistic_service
from app.core.dependencies.admin import (
    get_category_progress_info_service,
    get_level_service,
)
from app.schemas.common import UserOut
from app.services.common import StatisticService
from app.services.admin import CategoryProgressInfoService, LevelService
from app.schemas.client import LevelProgressByCategoryStatistic, ProgressByUserStatistic

router = APIRouter(tags=["statistics"])


@router.get(
    "/statistics/category-current-progress/{category_id}",
    response_model=LevelProgressByCategoryStatistic,
    operation_id="getCategoryCurrentProgress",
)
async def get_category_current_progress(
    category_id: int,
    current_user: UserOut = Depends(get_current_user),
    svc_statistic: StatisticService = Depends(get_statistic_service),
    svc_category_progress_info: CategoryProgressInfoService = Depends(
        get_category_progress_info_service
    ),
    svc_level: LevelService = Depends(get_level_service),
):
    cpi = await svc_category_progress_info.get_top_category_progress_info(
        user_id=current_user.id, category_id=category_id
    )

    progress = await svc_statistic.get_level_progress_by_category(
        user_id=current_user.id, category_id=category_id, level_id=cpi.level_id
    )

    next_level = await svc_level.get_next_level(cpi.level_id)

    return LevelProgressByCategoryStatistic(
        progress=progress,
        current_level=cpi.level.alias,
        next_level=next_level.alias if next_level else None,
    )


@router.get(
    "/statistics/progress/",
    response_model=ProgressByUserStatistic,
    operation_id="getProgressByUser",
)
async def get_progress_by_user(
    current_user: UserOut = Depends(get_current_user),
    svc_statistic: StatisticService = Depends(get_statistic_service),
):
    progress = await svc_statistic.get_progress_by_user(user_id=current_user.id)

    return ProgressByUserStatistic(progress=progress)


@router.get(
    "/statistics/today_progress/",
    response_model=ProgressByUserStatistic,
    operation_id="getTodayProgressByUser",
)
async def get_today_progress_by_user(
    current_user: UserOut = Depends(get_current_user),
    svc_statistic: StatisticService = Depends(get_statistic_service),
):
    progress = await svc_statistic.get_today_progress_by_user(user_id=current_user.id)

    return ProgressByUserStatistic(progress=progress)
