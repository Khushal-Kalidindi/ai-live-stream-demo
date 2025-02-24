import requests

url = "http://localhost:5000/add_scheduled_stream"

payload = {
    "streamer_name": "Anthony",
    "video_url": "jfKfPfyJRdk",
    "stream_title": "24/7 USC LoFi Study Sesh",
    "stream_description": "",
    "start_time": "03:00",
    "end_time": "03:10",
    "tags": ["Chill", "Study", "Productive"],
    "chapters": [],  # Left empty since no chapters were provided
}

headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
