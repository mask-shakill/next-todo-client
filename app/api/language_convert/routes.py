from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from .models import TextToSpeechRequest
from .utils import TextToSpeechUtil
import os

router = APIRouter()
tts_util = TextToSpeechUtil()

def cleanup_file(filepath: str):
    """Background task to cleanup the file after sending."""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f"Error cleaning up file {filepath}: {e}")

@router.post("/convert")
async def convert_text_to_speech(request: TextToSpeechRequest, background_tasks: BackgroundTasks):
    """
    Convert text to speech and return as downloadable file.
    Default download filename is shakil.mp3
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        # Generate speech file
        filepath, detected_lang = await tts_util.generate_speech(request.text, request.voice_type)
        
        # Add cleanup task to background tasks
        background_tasks.add_task(cleanup_file, filepath)
        
        # Return file response with fixed filename shakil.mp3
        return FileResponse(
            filepath,
            media_type="audio/mpeg",
            filename="shakil.mp3",
            headers={
                "Content-Disposition": "attachment; filename=shakil.mp3",
                "X-Detected-Language": detected_lang
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Speech generation failed: {str(e)}"
        )