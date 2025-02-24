import os
from typing import Tuple
import uuid
from fastapi import HTTPException
from langdetect import detect
import edge_tts
import asyncio
from .models import SpeakerVoice

class SpeechGenerator:
    def __init__(self):
        self.storage = "audio_files"
        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

    async def get_language(self, message: str) -> str:
        try:
            loop = asyncio.get_event_loop()
            lang = await loop.run_in_executor(None, detect, message)
            return lang
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def select_voice(self, language: str, speaker: SpeakerVoice) -> str:
        voices = {
            'bn': {
                SpeakerVoice.MALE: 'bn-IN-BashkarNeural',
                SpeakerVoice.FEMALE: 'bn-IN-TanishaaNeural',
                SpeakerVoice.ROBOTIC: 'bn-IN-BashkarNeural',
                SpeakerVoice.NEUTRAL: 'bn-IN-TanishaaNeural'
            },
            'en': {
                SpeakerVoice.MALE: 'en-US-ChristopherNeural',
                SpeakerVoice.FEMALE: 'en-US-JennyNeural',
                SpeakerVoice.ROBOTIC: 'en-US-RogerNeural',
                SpeakerVoice.NEUTRAL: 'en-US-AriaNeural'
            },
            'hi': {
                SpeakerVoice.MALE: 'hi-IN-MadhurNeural',
                SpeakerVoice.FEMALE: 'hi-IN-SwaraNeural',
                SpeakerVoice.ROBOTIC: 'hi-IN-MadhurNeural',
                SpeakerVoice.NEUTRAL: 'hi-IN-SwaraNeural'
            }
        }
        
        default_lang = 'en'
        if language not in voices:
            if language.startswith('bn'): default_lang = 'bn'
            
        return voices[default_lang][speaker]

    async def create_speech(self, message: str, speaker: SpeakerVoice) -> Tuple[str, str]:
        try:
            language = await self.get_language(message)
            voice = self.select_voice(language, speaker)
            audio_path = os.path.join(self.storage, f"{uuid.uuid4()}.mp3")
            
            communicator = edge_tts.Communicate(message, voice)
            await communicator.save(audio_path)
            
            return audio_path, language

        except Exception as e:
            if 'audio_path' in locals() and os.path.exists(audio_path):
                os.remove(audio_path)
            raise HTTPException(status_code=500, detail=str(e))