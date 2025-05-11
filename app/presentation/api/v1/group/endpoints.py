from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from app.domain.entities.group import Group
from app.presentation.api.v1.dependencies import get_group_service

router = APIRouter()


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[Group],
)
async def get_groups(
        name: str | None = None,
        group_service=Depends(get_group_service),
):
    return await group_service.get_list(name_filter=name)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=Group,
)
async def create_group(
        name: str,
        group_service=Depends(get_group_service),
):
    return await group_service.create(name)


@router.get(
    "/{group_id}",
    status_code=status.HTTP_200_OK,
    response_model=Group,
)
async def get_group(
        group_id: UUID,
        group_service=Depends(get_group_service),
):
    return await group_service.get_by_id(group_id)
