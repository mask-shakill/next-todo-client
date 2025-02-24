from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from .models import TextToSpeechRequest
from .utils import TextToSpeechUtil

import os

router = APIRouter()
tts_service = TextToSpeechUtil()

def remove_file(filepath: str):
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as error:
        print(f"File cleanup error: {error}")

@router.post("/convert")
async def text_to_speech(request: TextToSpeechRequest, background_tasks: BackgroundTasks):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    try:
        audio_path, detected_language = await tts_service.generate_speech(request.text, request.voice_type)
        background_tasks.add_task(remove_file, audio_path)

        return FileResponse(
            path=audio_path,
            media_type="audio/mpeg",
            filename="shakil.mp3",
            headers={
                "Content-Disposition": "attachment; filename=output.mp3",
                "X-Detected-Language": detected_language
            }
        )
    
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Speech synthesis failed: {error}")
