from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class RetrieveAudioFileResponse(BaseModel):
    """
    Response model containing the URL or direct stream of the requested MP3 audio file.
    """

    file_url: str
    file_type: str
    mime_type: str


async def retrieve_audio_file(id: str) -> RetrieveAudioFileResponse:
    """
    Provides access to download the generated MP3 file.

    This function retrieves information about an audio file generated from a TTS request.
    It uses the TTSRequest ID to find the corresponding AudioOutput entry in the database,
    and constructs a response with the URL where the MP3 file can be accessed.

    Args:
        id (str): Unique identifier for the TTSRequest to retrieve the audio file for.

    Returns:
        RetrieveAudioFileResponse: Response model containing the URL or direct stream of the requested MP3 audio file.
    """
    audio_output: Optional[
        prisma.models.AudioOutput
    ] = await prisma.models.AudioOutput.prisma().find_unique(where={"ttsRequestId": id})
    if audio_output and audio_output.fileType == prisma.enums.AudioFileType.MP3:
        basePath = "http://localhost/files/"
        file_url = f"{basePath}{audio_output.filePath}"
        return RetrieveAudioFileResponse(
            file_url=file_url, file_type="MP3", mime_type="audio/mpeg"
        )
    else:
        return RetrieveAudioFileResponse(file_url="", file_type="", mime_type="")
