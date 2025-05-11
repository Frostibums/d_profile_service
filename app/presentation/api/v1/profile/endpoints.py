from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.domain.dto.profile import ProfileUpdateDTO
from app.presentation.api.v1.dependencies import get_profile_repo, get_profile_service
from app.presentation.api.v1.profile.schemas import ProfileOutput, ProfileUpdate

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
    response_model=list[ProfileOutput],
)
async def get_profiles(
        profile_service=Depends(get_profile_service),
):
    return await profile_service.get_list()


@router.get(
    "/group/{group_id}",
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
    "/{profile_id}",
    status_code=status.HTTP_200_OK,
)
async def update_profile(
        profile_id: str,
        update_data: ProfileUpdate,
        profile_service=Depends(get_profile_service),
):
    await profile_service.update(
        profile_id=profile_id,
        update_data=ProfileUpdateDTO(**update_data.model_dump()),
    )
