from fastapi import Depends
from fastapi.routing import APIRouter

from punq import Container

from application.api.v1.health.schemas import HealthOut
from infra.repositories.base import BaseMessagesRepository
from logic.init import init_container


router = APIRouter(
    tags=['Health'],
)


@router.get(
    '/health',
    tags=['Health'],
    response_model=HealthOut,
)
async def health_check(
    container: Container = Depends(dependency=init_container),
) -> dict[str, str | dict[str, str]]:
    """Performs a system-wide health check, including MongoDB and system stats."""
    try:
        await container.resolve(BaseMessagesRepository).mongo_db_client.admin.command(
            'ping'
        )  # MongoDB health check
        mongo_status = 'ok'
    except Exception as e:
        mongo_status = f'error: {str(e)}'

    return {
        'status': 'healthy' if mongo_status == 'Ok' else 'MongoDB is down',
        'detail': {
            'mongodb': mongo_status,
        },
    }
