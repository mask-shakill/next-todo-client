# app/api/language_convert/models.py

from pydantic import BaseModel, Field
from typing import Optional

class TextToSpeechRequest(BaseModel):
    text: str = Field(..., description="Text to convert to speech")
    download: Optional[bool] = Field(default=False, description="Whether to download the file")

class TextToSpeechResponse(BaseModel):
    success: bool
    message: str
    language: str
    file_path: Optional[str] = None