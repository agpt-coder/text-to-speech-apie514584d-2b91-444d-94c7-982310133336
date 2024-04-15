import os
from typing import Optional

import pyttsx3
from pydantic import BaseModel


class SynthesizeSpeechResponse(BaseModel):
    """
    Response model providing details about the task result, including the path to the generated audio file.
    """

    success: bool
    message: str
    audio_file_path: str


def synthesize_speech(
    user_id: str,
    text_input: str,
    ssml_input: Optional[str],
    voice_type: Optional[str],
    speed: Optional[float],
    pitch: Optional[float],
    volume: Optional[float],
) -> SynthesizeSpeechResponse:
    """
    Converts text input to speech audio with customized voice parameters.

    Args:
    user_id (str): The unique identifier for the user making the request.
    text_input (str): The plain text input to be converted into speech.
    ssml_input (Optional[str]): The SSML formatted input for more complex speech synthesis requirements.
    voice_type (Optional[str]): Specifies the desired voice type for the output speech.
    speed (Optional[float]): Defines the rate of speech output.
    pitch (Optional[float]): Adjusts the pitch of the speech output.
    volume (Optional[float]): Controls the volume of the generated speech.

    Returns:
    SynthesizeSpeechResponse: Response model providing details about the task result, including the path to the generated audio file.
    """
    try:
        engine = pyttsx3.init()
        if voice_type:
            voices = engine.getProperty("voices")
            engine.setProperty(
                "voice", voices[0].id if voice_type == "male" else voices[1].id
            )
        if speed:
            engine.setProperty("rate", int(speed))
        if pitch:
            engine.setProperty("pitch", pitch)
        if volume:
            engine.setProperty("volume", volume)
        file_name = f"{user_id}.mp3"
        audio_file_path = os.path.join("speech_outputs", file_name)
        engine.save_to_file(text_input if text_input else ssml_input, audio_file_path)
        engine.runAndWait()
        return SynthesizeSpeechResponse(
            success=True,
            message="Speech synthesis succeeded",
            audio_file_path=audio_file_path,
        )
    except Exception as e:
        return SynthesizeSpeechResponse(
            success=False, message=str(e), audio_file_path=""
        )
