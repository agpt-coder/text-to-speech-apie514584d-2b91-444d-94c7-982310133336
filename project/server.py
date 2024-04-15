import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.api_integration_details_service
import project.authenticate_user_service
import project.create_user_service
import project.retrieve_audio_file_service
import project.synthesize_speech_service
import project.update_user_profile_service
import project.update_voice_profile_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="Text-to-Speech API",
    lifespan=lifespan,
    description="The project entails building an endpoint that can accept plain text or SSML formatted input, convert this input into natural-sounding speech audio utilizing Python libraries, and allow the customization of various voice parameters such as voice type, speed, pitch, volume, and potentially other parameters like strategic pauses for enhanced clarity and emotional impact. The preferred Python package for the text-to-speech conversion process is pyttsx3 due to its offline capabilities and extensive customization features, including voice type (neutral preferred), rate (speed), and volume adjustments. Additionally, the generated audio file should be available in MP3 format, which suits the user's needs. Essential insights and requirements gathered from the interview process include the importance of customization in the text-to-speech process to create a more engaging and natural auditory experience. Libraries such as gTTS and SpeechRecognition were also identified as relevant for text-to-speech and speech-to-text conversions but were not selected due to the project's specific requirements and the need for offline functionality.",
)


@app.post(
    "/tts/synthesize",
    response_model=project.synthesize_speech_service.SynthesizeSpeechResponse,
)
async def api_post_synthesize_speech(
    user_id: str,
    text_input: str,
    ssml_input: Optional[str],
    voice_type: Optional[str],
    speed: Optional[float],
    pitch: Optional[float],
    volume: Optional[float],
) -> project.synthesize_speech_service.SynthesizeSpeechResponse | Response:
    """
    Converts text input to speech audio with customized voice parameters.
    """
    try:
        res = project.synthesize_speech_service.synthesize_speech(
            user_id, text_input, ssml_input, voice_type, speed, pitch, volume
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/users/register", response_model=project.create_user_service.CreateUserResponse
)
async def api_post_create_user(
    email: str, password: str
) -> project.create_user_service.CreateUserResponse | Response:
    """
    Registers a new user with email and password.
    """
    try:
        res = await project.create_user_service.create_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/users/login",
    response_model=project.authenticate_user_service.AuthenticateUserResponse,
)
async def api_post_authenticate_user(
    email: str, password: str
) -> project.authenticate_user_service.AuthenticateUserResponse | Response:
    """
    Authenticates a user and returns an access token.
    """
    try:
        res = await project.authenticate_user_service.authenticate_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/integration/details",
    response_model=project.api_integration_details_service.APIIntegrationDetailsResponse,
)
async def api_get_api_integration_details() -> project.api_integration_details_service.APIIntegrationDetailsResponse | Response:
    """
    Returns API integration capabilities and documentation links.
    """
    try:
        res = project.api_integration_details_service.api_integration_details()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/audio/{id}",
    response_model=project.retrieve_audio_file_service.RetrieveAudioFileResponse,
)
async def api_get_retrieve_audio_file(
    id: str,
) -> project.retrieve_audio_file_service.RetrieveAudioFileResponse | Response:
    """
    Provides access to download the generated MP3 file.
    """
    try:
        res = await project.retrieve_audio_file_service.retrieve_audio_file(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/voice/customize",
    response_model=project.update_voice_profile_service.VoiceCustomizationResponse,
)
async def api_post_update_voice_profile(
    user_id: str, voice_type: str, speed: float, pitch: float, volume: float
) -> project.update_voice_profile_service.VoiceCustomizationResponse | Response:
    """
    Saves or updates a user's voice customization preferences.
    """
    try:
        res = await project.update_voice_profile_service.update_voice_profile(
            user_id, voice_type, speed, pitch, volume
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/users/{id}/update",
    response_model=project.update_user_profile_service.UserProfileUpdateResponse,
)
async def api_put_update_user_profile(
    id: str,
    email: Optional[str],
    username: Optional[str],
    voice_profile: Optional[str],
    password: Optional[str],
) -> project.update_user_profile_service.UserProfileUpdateResponse | Response:
    """
    Updates user profile information.
    """
    try:
        res = await project.update_user_profile_service.update_user_profile(
            id, email, username, voice_profile, password
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
