import prisma
import prisma.models
from pydantic import BaseModel


class VoiceProfile(BaseModel):
    """
    Contains the user's updated voice customization settings.
    """

    voice_type: str
    speed: float
    pitch: float
    volume: float


class VoiceCustomizationResponse(BaseModel):
    """
    Confirms the successful update of voice customization preferences and returns the updated preferences for the user.
    """

    success: bool
    updated_preferences: VoiceProfile


async def update_voice_profile(
    user_id: str, voice_type: str, speed: float, pitch: float, volume: float
) -> VoiceCustomizationResponse:
    """
    Saves or updates a user's voice customization preferences.

    The function checks if an existing voice profile for the given user ID exists.
    If it does, it updates the voice profile with the new settings.
    If it does not, it creates a new voice profile for the user with the provided settings.
    Finally, it constructs and returns a response indicating the success of the operation and the updated preferences.

    Args:
        user_id (str): The identifier of the user to update voice preferences for.
        voice_type (str): User's preferred voice type for speech synthesis.
        speed (float): Speed level for speech output.
        pitch (float): Pitch level for speech synthesis.
        volume (float): Volume level for speech output.

    Returns:
        VoiceCustomizationResponse: Confirms the successful update of voice customization preferences and returns the updated preferences for the user.
    """
    existing_profile = await prisma.models.VoiceProfile.prisma().find_unique(
        where={"userId": user_id}
    )
    if existing_profile:
        updated_profile = await prisma.models.VoiceProfile.prisma().update(
            where={"id": existing_profile.id},
            data={
                "voiceType": voice_type,
                "speed": speed,
                "pitch": pitch,
                "volume": volume,
            },
        )
    else:
        updated_profile = await prisma.models.VoiceProfile.prisma().create(
            data={
                "userId": user_id,
                "voiceType": voice_type,
                "speed": speed,
                "pitch": pitch,
                "volume": volume,
            }
        )
    response = VoiceCustomizationResponse(
        success=True,
        updated_preferences=VoiceProfile(
            voice_type=updated_profile.voiceType,
            speed=updated_profile.speed,
            pitch=updated_profile.pitch,
            volume=updated_profile.volume,
        ),
    )
    return response
