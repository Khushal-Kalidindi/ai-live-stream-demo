import json
import requests
import base64
from dotenv import load_dotenv
import os

load_dotenv()

# Get the Eden AI API key from the environment variables
edenai_api_key = os.getenv("EDENAI_API")
if not edenai_api_key:
    raise ValueError("Please set the EDENAI_API environment variable")


headers = {"Authorization": "Bearer "}

url = "https://api.edenai.run/v2/audio/text_to_speech"
payload = {
    "providers": "elevenlabs", "language": "en-US",
    "option": "FEMALE",
    "text": "hi devin, how are you doing today?",
}

response = requests.post(url, json=payload, headers=headers)

result = json.loads(response.text)
# audio_url = result['google']['audio_resource_url']
# audio_response = requests.get(audio_url)

# if audio_response.status_code == 200:
#     try:
#         decoded = base64.b64decode(audio_response.content)
#         with open("audio.mp3", "wb") as f:
#             f.write(decoded)

audio_base64 = result['elevenlabs']['audio']
decoded = base64.b64decode(audio_base64)
with open("static/audio.mp3", "wb") as f:
    f.write(decoded)
print("Audio file saved as audio.mp3")

