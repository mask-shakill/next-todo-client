from typing import Dict
from langdetect import detect
from .models import VoiceType
import asyncio

class TextToSpeechService:
    def __init__(self):
        pass

    async def detect_language(self, text: str) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, detect, text)

    def get_voice_by_type(self, lang_code: str, voice_type: VoiceType) -> str:
        voice_mappings: Dict[str, Dict[VoiceType, str]] = {
            "bn": {
                VoiceType.MALE: "bn-IN-BashkarNeural",
                VoiceType.FEMALE: "bn-IN-TanishaaNeural",
                VoiceType.ROBOTIC: "bn-IN-BashkarNeural",
                VoiceType.NEUTRAL: "bn-IN-TanishaaNeural",
            },
            "en": {
                VoiceType.MALE: "en-US-ChristopherNeural",
                VoiceType.FEMALE: "en-US-JennyNeural",
                VoiceType.ROBOTIC: "en-US-RogerNeural",
                VoiceType.NEUTRAL: "en-US-AriaNeural",
            },
            "hi": {
                VoiceType.MALE: "hi-IN-MadhurNeural",
                VoiceType.FEMALE: "hi-IN-SwaraNeural",
                VoiceType.ROBOTIC: "hi-IN-MadhurNeural",
                VoiceType.NEUTRAL: "hi-IN-SwaraNeural",
            },
        }

        lang_code = "bn" if lang_code.startswith("bn") else voice_mappings.get(lang_code, "en")
        return voice_mappings[lang_code][voice_type]
