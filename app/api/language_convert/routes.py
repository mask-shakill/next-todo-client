# app/api/language_convert/routes.py

from fastapi import APIRouter, HTTPException, Response, Request
from fastapi.responses import FileResponse, JSONResponse
from .models import TextToSpeechRequest, TextToSpeechResponse
from .service import TextToSpeechService
import os

router = APIRouter()
tts_service = TextToSpeechService()

@router.post("/convert")
async def convert_text_to_speech(request: TextToSpeechRequest):
    """
    Convert text to speech with automatic language detection.
    If download=True, returns audio file for download.
    If download=False, returns audio file for playing in browser.
    """
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty"
        )

    result = await tts_service.convert_text_to_speech(request.text)
    filepath = result["filepath"]
    
    headers = {
        "X-Detected-Language": result["detected_language"],
        "X-File-Size": str(result["file_size"])
    }
    
    if request.download:
        # Return file as attachment for downloading
        return FileResponse(
            filepath,
            media_type="audio/mpeg",
            headers=headers,
            filename="speech.mp3",
            background=lambda: tts_service.tts_util.cleanup_audio_file(filepath, True)
        )
    else:
        # Return file for playing in browser
        return FileResponse(
            filepath,
            media_type="audio/mpeg",
            headers=headers,
            background=lambda: tts_service.tts_util.cleanup_audio_file(filepath, True)
        )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}