# app/api/language_convert/utils.py

import os
from typing import Tuple
import uuid
from fastapi import HTTPException
from langdetect import detect
import asyncio
import edge_tts

class TextToSpeechUtil:
    def __init__(self):
        self.audio_dir = "audio_files"
        if not os.path.exists(self.audio_dir):
            os.makedirs(self.audio_dir)

    async def detect_language(self, text: str) -> str:
        """Detect the language of input text."""
        try:
            loop = asyncio.get_event_loop()
            lang = await loop.run_in_executor(None, detect, text)
            return lang
        except Exception as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Language detection failed: {str(e)}"
            )

    async def generate_speech(self, text: str) -> Tuple[str, str]:
        """Generate speech from text using Edge TTS."""
        try:
            # Detect language
            detected_lang = await self.detect_language(text)
            
            # Map language code to voice
            voice = self._get_voice_for_language(detected_lang)
            
            # Generate unique filename
            filename = f"{uuid.uuid4()}.mp3"
            filepath = os.path.join(self.audio_dir, filename)
            
            # Generate speech using Edge TTS
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(filepath)
            
            return filepath, detected_lang
        except Exception as e:
            if 'filepath' in locals() and os.path.exists(filepath):
                os.remove(filepath)
            raise HTTPException(
                status_code=500,
                detail=f"Speech generation failed: {str(e)}"
            )

    def _get_voice_for_language(self, lang_code: str) -> str:
        """Map language codes to Edge TTS voices."""
        voice_map = {
            'en': 'en-US-EricNeural',
            'es': 'es-ES-AlvaroNeural',
            'fr': 'fr-FR-HenriNeural',
            'de': 'de-DE-ConradNeural',
            'it': 'it-IT-DiegoNeural',
            'pt': 'pt-BR-AntonioNeural',
            'hi': 'hi-IN-MadhurNeural',
            'bn': 'bn-IN-BashkarNeural',
            'ja': 'ja-JP-KeitaNeural',
            'ko': 'ko-KR-InJoonNeural',
            'zh': 'zh-CN-YunxiNeural',
            'ru': 'ru-RU-DmitryNeural',
            'ar': 'ar-SA-HamedNeural',
        }
        return voice_map.get(lang_code, 'en-US-EricNeural')

    def get_file_size(self, filepath: str) -> int:
        """Get file size in bytes."""
        return os.path.getsize(filepath)

    def cleanup_audio_file(self, filepath: str, force: bool = False):
        """Remove the audio file after it has been sent to the client."""
        try:
            if os.path.exists(filepath) and force:
                os.remove(filepath)
        except Exception as e:
            print(f"Error cleaning up file {filepath}: {str(e)}")