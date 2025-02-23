import requests

url = "http://localhost:5000/add_scheduled_stream"

payload = {
    "streamer_name": "Alexa",
    "video_url": "https://www.youtube.com/watch?v=BdhqubW1GJE",
    "stream_title": "",
    "stream_description": "",
    "start_time": "03:00",
    "end_time": "03:10",
    "tags": ["Quick", "At-Home", "Beginner-Friendly"],
    "chapters": [
        {"timestamp": "00:00", "description": "Get Ready!"},
        {"timestamp": "00:20", "description": "Leg Switches"},
        {"timestamp": "01:20", "description": "Reverse Crunch + Leg Opener"},
        {"timestamp": "02:20", "description": "Leg Lowers"},
        {"timestamp": "03:20", "description": "Scissor Crossovers"},
        {"timestamp": "04:20", "description": "Cross Crunches"},
        {"timestamp": "05:20", "description": "Butterfly Crunches"},
        {"timestamp": "06:20", "description": "Single Leg Extensions"},
        {"timestamp": "07:20", "description": "Heel Taps"},
        {"timestamp": "08:20", "description": "Plank Knee Tucks"},
        {"timestamp": "09:20", "description": "Spider Crunches"},
    ],
}

headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
