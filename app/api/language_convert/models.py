from pydantic import BaseModel, Field # type: ignore
from enum import Enum

class VoiceType(str, Enum):
    MALE = "male"
    FEMALE = "female"
    ROBOTIC = "robotic"
    NEUTRAL = "neutral"

class TextToSpeechRequest(BaseModel):
    text: str = Field(..., description="Text to convert to speech")
    voice_type: VoiceType = Field(default=VoiceType.MALE, description="Type of voice to use")