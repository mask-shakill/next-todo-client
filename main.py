# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.language_convert.routes import router as tts_router
from app.api.language_convert.middleware import ProcessTimeMiddleware

app = FastAPI(
    title="Text to Speech API",
    description="API for converting text to natural-sounding speech with automatic language detection",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(ProcessTimeMiddleware)

# Add routes
app.include_router(tts_router, prefix="/api/tts", tags=["text-to-speech"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)