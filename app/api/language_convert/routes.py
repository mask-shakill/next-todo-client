from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from .models import SpeechRequest
from .utils import SpeechGenerator
import os

router = APIRouter()
generator = SpeechGenerator()

def remove_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

@router.post("/convert")
async def create_audio(data: SpeechRequest, tasks: BackgroundTasks):
    if not data.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")

    try:
        audio_path, language = await generator.create_speech(data.message, data.speaker)
        tasks.add_task(remove_file, audio_path)
        
        return FileResponse(
            audio_path,
            media_type="audio/mpeg",
            filename="shakil.mp3",
            headers={"X-Language": language}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))