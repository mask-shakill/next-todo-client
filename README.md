# Text to Speech Converter API

A FastAPI-based text-to-speech converter that supports multiple languages and voice types. The API automatically detects the input language and generates natural-sounding speech using Microsoft Edge's TTS engine.

## Features

- Multiple language support (Bengali, English, Hindi)
- Multiple voice types (Male, Female, Robotic, Neutral)
- Automatic language detection
- Direct MP3 file download
- Asynchronous processing
- Error handling with fallback options

## Project Structure

```
language_conversion/
├── app/
│   ├── __init__.py
│   └── api/
│       └── language_convert/
│           ├── __init__.py
│           ├── models.py
│           ├── routes.py
│           ├── utils.py
├── audio_files/
├── main.py
└── requirements.txt
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd language_conversion
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:

```bash
uvicorn main:app --reload
```

2. API Endpoints:
   - Convert text to speech: `POST /api/text-speech/convert`

### API Request Format

```json
{
  "message": "Your text message here",
  "speaker": "male" // Options: "male", "female", "robotic", "neutral"
}
```

### Example Usage

Using curl:

```bash
curl -X POST 'http://127.0.0.1:8000/api/tts/convert' \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "Hello, how are you?",
    "speaker": "male"
  }' \
  --output shakil.mp3
```

Using Python requests:

```python
import requests

url = "http://127.0.0.1:8000/api/tts/convert"
data = {
    "message": "Hello, how are you?",
    "speaker": "male"
}

response = requests.post(url, json=data)
with open("shakil.mp3", "wb") as f:
    f.write(response.content)
```

## Supported Languages

1. Bengali (bn)

   - Male: bn-IN-BashkarNeural
   - Female: bn-IN-TanishaaNeural

2. English (en)

   - Male: en-US-GuyNeural
   - Female: en-US-JennyNeural
   - Robotic: en-US-RogerNeural
   - Neutral: en-US-AriaNeural

3. Hindi (hi)
   - Male: hi-IN-MadhurNeural
   - Female: hi-IN-SwaraNeural

## Error Handling

The API includes robust error handling:

- Language detection errors
- Audio generation failures
- Automatic fallback for Bengali text
- Empty message validation
- File system error handling

## Response Headers

The API returns useful information in response headers:

- `X-Language`: Detected language code
- `Content-Type`: audio/mpeg
- `Content-Disposition`: attachment; filename=shakil.mp3

## Development

To add new languages or voices:

1. Update the voice mappings in `utils.py`
2. Add language support in the `select_voice` method
3. Update documentation accordingly

## Dependencies

- FastAPI: Web framework
- edge-tts: Text-to-speech engine
- langdetect: Language detection
- uvicorn: ASGI server
- python-multipart: Form data handling
- pydantic: Data validation

## Notes

- Generated audio files are automatically cleaned up after sending
- The API uses Microsoft Edge's TTS engine for high-quality speech synthesis
- Default output filename is always "shakil.mp3"
- All responses are in MP3 format

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Shahriar Kobir Shakil  
GitHub: [[Your GitHub Profile URL](https://github.com/mask-shakill)]
