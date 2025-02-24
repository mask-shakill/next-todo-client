from typing import Dict
from langdetect import detect
from .models import VoiceType
import asyncio

class TextToSpeechService:
    def __init__(self):
        pass

    async def detect_language(self, text: str) -> str:
        """Detect language of input text."""
        loop = asyncio.get_event_loop()
        lang = await loop.run_in_executor(None, detect, text)
        return lang

    def get_voice_by_type(self, lang_code: str, voice_type: VoiceType) -> str:
        """Get appropriate voice based on language and type."""
        voice_mappings = {
            'bn': {  # Bengali
                VoiceType.MALE: 'bn-IN-BashkarNeural',
                VoiceType.FEMALE: 'bn-IN-TanishaaNeural',
                VoiceType.ROBOTIC: 'bn-IN-BashkarNeural',
                VoiceType.NEUTRAL: 'bn-IN-TanishaaNeural'
            },
            'en': {  # English
                VoiceType.MALE: 'en-US-ChristopherNeural',
                VoiceType.FEMALE: 'en-US-JennyNeural',
                VoiceType.ROBOTIC: 'en-US-RogerNeural',
                VoiceType.NEUTRAL: 'en-US-AriaNeural'
            },
            'hi': {  # Hindi
                VoiceType.MALE: 'hi-IN-MadhurNeural',
                VoiceType.FEMALE: 'hi-IN-SwaraNeural',
                VoiceType.ROBOTIC: 'hi-IN-MadhurNeural',
                VoiceType.NEUTRAL: 'hi-IN-SwaraNeural'
            }
        }
        
        # If language not found in mappings, check if it's Bengali
        if lang_code not in voice_mappings:
            if lang_code.startswith('bn'):
                lang_code = 'bn'
            else:
                lang_code = 'en'  # Default to English
        
        lang_voices = voice_mappings[lang_code]
        return lang_voices[voice_type]