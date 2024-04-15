from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class User(BaseModel):
    """
    The user object model reflecting various attributes of a user such as email, username, and associated voice profile ID.
    """

    id: str
    email: str
    username: str
    voice_profile_id: Optional[str] = None


class UserProfileUpdateResponse(BaseModel):
    """
    Response object for the update user profile endpoint. Indicates success and contains the updated user profile data.
    """

    success: bool
    user: User


async def update_user_profile(
    id: str,
    email: Optional[str] = None,
    username: Optional[str] = None,
    voice_profile: Optional[str] = None,
    password: Optional[str] = None,
) -> UserProfileUpdateResponse:
    """
    Updates user profile information based on provided arguments.

    Args:
        id (str): The unique identifier of the user whose profile is being updated.
        email (Optional[str]): The new email address of the user, if updating.
        username (Optional[str]): The new username, if updating.
        voice_profile (Optional[str]): The ID of the new voice profile to associate with the user, if updating.
        password (Optional[str]): The new password, if updating.

    Returns:
        UserProfileUpdateResponse: Contains the result of the update operation including success status and user info.

    This function will return a user profile update response object. It checks each argument, and if provided, it updates
    the corresponding field in the user's profile.
    """
    update_data = {}
    if email:
        update_data["email"] = email
    if username:
        update_data["username"] = username
    if password:
        update_data["password"] = password
    if voice_profile:
        update_data["VoiceProfiles"] = {"connect": {"id": voice_profile}}
    updated_user = await prisma.models.User.prisma().update(
        where={"id": id}, data=update_data, include={"VoiceProfiles": True}
    )
    voice_profile_id = (
        updated_user.voice_profile_id if voice_profile else None
    )  # TODO(autogpt): Cannot access member "voice_profile_id" for type "User"
    #     Member "voice_profile_id" is unknown. reportAttributeAccessIssue
    user_info = User(
        id=updated_user.id,
        email=updated_user.email,
        username=updated_user.username,
        voice_profile_id=voice_profile_id,
    )  # TODO(autogpt): Cannot access member "username" for type "User"
    #     Member "username" is unknown. reportAttributeAccessIssue
    return UserProfileUpdateResponse(success=True, user=user_info)
