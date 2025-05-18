from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.domain.dto.profile import ProfileUpdateDTO
from app.infrastructure.bus.kafka.producer import KafkaEventProducer
from app.presentation.api.v1.dependencies import (
    get_producer,
    get_profile_repo,
    get_profile_service, get_current_user_id,
)
from app.presentation.api.v1.profile.schemas import ProfileOutput, ProfileUpdate
from app.service.profile import ProfileService

router = APIRouter()


@router.post(
    "/{user_id}/group/{group_id}",
    status_code=status.HTTP_200_OK,
)
async def assign_user_to_group(
        group_id: UUID,
        user_id: UUID,
        profile_service=Depends(get_profile_service),
):
    await profile_service.assign_to_group(user_id, group_id)


@router.delete(
    "/{user_id}/group/{group_id}",
    status_code=status.HTTP_200_OK,
)
async def remove_user_from_group(
        group_id: UUID,
        user_id: UUID,
        profile_service=Depends(get_profile_service),
):
    await profile_service.remove_from_group(user_id, group_id)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ProfileOutput,
)
async def get_current_user_profile(
        user_id: UUID = Depends(get_current_user_id),
        profile_service: ProfileService = Depends(get_profile_service),
):
    profile = await profile_service.get_by_user_id(user_id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile for such user not found.",
        )
    return profile


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=list[ProfileOutput],
)
async def get_profiles(
        profile_service=Depends(get_profile_service),
):
    return await profile_service.get_list()


@router.get(
    "/by-group/{group_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[ProfileOutput],
)
async def get_profiles_by_group(
        group_id: UUID,
        profile_service=Depends(get_profile_service),
):
    profiles = await profile_service.get_by_group(
        group_id=group_id,
    )
    return profiles


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProfileOutput,
)
async def get_profile(
        user_id: str,
        profile_repo=Depends(get_profile_repo),
):
    profile = await profile_repo.get_by_user_id(
        user_id=user_id,
    )
    if not profile:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return profile


@router.patch(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProfileOutput,
)
async def update_profile(
        user_id: UUID,
        update_data: ProfileUpdate,
        profile_service: ProfileService = Depends(get_profile_service),
):
    updated_profile = await profile_service.update(
        user_id=user_id,
        update_data=ProfileUpdateDTO(
            **update_data.model_dump(
                exclude_unset=True,
                exclude_defaults=True,
            )
        ),
    )
    if not updated_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    return updated_profile
