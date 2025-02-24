# app/api/language_convert/service.py

from .utils import TextToSpeechUtil
from typing import Dict

class TextToSpeechService:
    def __init__(self):
        self.tts_util = TextToSpeechUtil()

    async def convert_text_to_speech(self, text: str) -> Dict:
        """Convert text to speech and return file information."""
        filepath, detected_lang = await self.tts_util.generate_speech(text)
        file_size = self.tts_util.get_file_size(filepath)
        
        return {
            "filepath": filepath,
            "detected_language": detected_lang,
            "file_size": file_size
        }