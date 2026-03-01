from fastapi import APIRouter, Depends

from app.core.dependencies.service_factories import (
    get_current_user,
    get_statistic_service,
)
from app.schemas.common import UserOut
from app.services.client import StatisticService
from app.schemas.client import ProgressByUserStatistic

router = APIRouter(tags=["statistics"])


@router.get(
    "/statistics/progress/",
    response_model=ProgressByUserStatistic,
    operation_id="getStatisticsProgress",
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
    operation_id="getStatisticsTodayProgress",
)
async def get_today_progress_by_user(
    current_user: UserOut = Depends(get_current_user),
    svc_statistic: StatisticService = Depends(get_statistic_service),
):
    progress = await svc_statistic.get_today_progress_by_user(user_id=current_user.id)

    return ProgressByUserStatistic(progress=progress)
