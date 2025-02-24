from pydantic import BaseModel, Field
from enum import Enum

class SpeakerVoice(str, Enum):
    MALE = "male"
    FEMALE = "female"
    ROBOTIC = "robotic"
    NEUTRAL = "neutral"

class SpeechRequest(BaseModel):
    message: str = Field(..., description="Text message to convert to speech")
    speaker: SpeakerVoice = Field(default=SpeakerVoice.MALE)