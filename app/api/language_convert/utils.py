import os
import uuid
import asyncio
from typing import Tuple
from fastapi import HTTPException
from langdetect import detect
import edge_tts
from .models import VoiceType

class TextToSpeech:
    def __init__(self):
        self.output_dir = "audio_files"
        os.makedirs(self.output_dir, exist_ok=True)

    async def detect_language(self, text: str) -> str:
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, detect, text)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Language detection failed: {str(e)}")

    def get_voice(self, lang_code: str, voice_type: VoiceType) -> str:
        voices = {
            'bn': {
                VoiceType.MALE: 'bn-IN-BashkarNeural',
                VoiceType.FEMALE: 'bn-IN-TanishaaNeural',
                VoiceType.ROBOTIC: 'bn-IN-BashkarNeural',
                VoiceType.NEUTRAL: 'bn-IN-TanishaaNeural'
            },
            'en': {
                VoiceType.MALE: 'en-US-ChristopherNeural',
                VoiceType.FEMALE: 'en-US-JennyNeural',
                VoiceType.ROBOTIC: 'en-US-RogerNeural',
                VoiceType.NEUTRAL: 'en-US-AriaNeural'
            },
            'hi': {
                VoiceType.MALE: 'hi-IN-MadhurNeural',
                VoiceType.FEMALE: 'hi-IN-SwaraNeural',
                VoiceType.ROBOTIC: 'hi-IN-MadhurNeural',
                VoiceType.NEUTRAL: 'hi-IN-SwaraNeural'
            }
        }
        lang_code = 'bn' if lang_code.startswith('bn') else voices.get(lang_code, voices['en'])
        return voices[lang_code][voice_type]

    async def generate_audio(self, text: str, voice_type: VoiceType) -> Tuple[str, str]:
        try:
            detected_lang = await self.detect_language(text)
            voice = self.get_voice(detected_lang, voice_type)
            filename = f"{uuid.uuid4()}.mp3"
            file_path = os.path.join(self.output_dir, filename)
            
            tts = edge_tts.Communicate(text, voice)
            await tts.save(file_path)
            
            return file_path, detected_lang
        except Exception as e:
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=500, detail=f"Speech generation failed: {str(e)}")
