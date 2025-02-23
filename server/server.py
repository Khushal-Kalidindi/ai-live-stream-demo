from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime
import pymongo
from pymongo import MongoClient
from flask_cors import CORS
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Initialize Flask app and SocketIO
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Get the MongoDB connection details from the environment variables
db_password = os.getenv("DB_PASSWORD")
if not db_password:
    raise ValueError("Please set the DB_PASSWORD environment variable")
db_username = os.getenv("DB_USERNAME")
if not db_username:
    raise ValueError("Please set the DB_USERNAME environment variable")
db_link_name = os.getenv("DB_LINK_NAME")
if not db_link_name:
    raise ValueError("Please set the DB_LINK_NAME environment variable")
db_name = os.getenv("DB_NAME")
if not db_name:
    raise ValueError("Please set the DB_NAME environment variable")

# MongoDB connection string
uri = f"mongodb+srv://{db_username}:{db_password}@{db_link_name}.ecxgt.mongodb.net/?retryWrites=true&w=majority&appName={db_name}"
# MongoDB client setup
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["chat_app"]
messages_collection = db["messages"]

# This is a sample route to check if server is running
@app.route('/')
def index():
    return "Flask server is running!"

# SocketIO event to handle sending and receiving messages
@socketio.on('send_message')
def handle_send_message(data):
    print(f"Received message from {data['username']}: {data['message']}")
    # Save message to MongoDB
    message = {
        "username": data['username'],
        "message": data['message'],
        "usernameColor": data['usernameColor'],
        "timestamp": str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    }
    messages_collection.insert_one(message)
    print(message)
    message.pop('_id', None)
    message.pop('timestamp', None)

    # Emit the message to all connected clients in real-time
    print("Emitting message to all clients..." + json.dumps(message))
    emit('receive_message', json.dumps(message), broadcast=True)

# SocketIO event to load the previous messages (if any)
@socketio.on('load_messages')
def handle_load_messages():
    print("Loading previous messages...")
    # Fetch all messages from the database
    messages = list(messages_collection.find().sort("timestamp", pymongo.ASCENDING))
    # # Convert the timestamp to a string format before sending the response
    # for message in messages:
    #     message["timestamp"] = message["timestamp"].strftime('%Y-%m-%d %H:%M:%S')
    messages = [{"username": msg["username"], "message": msg["message"], "usernameColor": msg["usernameColor"]} for msg in messages]
    
    # Send the messages to the client
    emit('load_previous_messages', messages)

# Create an api route to add a scheduled stream, which will be added to the database
# We will add to a collection called scheduled_streams
# The scheduled stream will have the following fields:
# - streamer_name (string)
# - video_url (string)
# - stream_title (string)
# - stream_description (string)
# - start_time (datetime)
# - end_time (datetime)
# - tags (list of strings)
# - chapters (list of objects), each object will have a timestamp and description
# Example of a chapter object: {"timestamp": "00:05:30", "description": "Introduction to first topic"}
@app.route('/add_scheduled_stream', methods=['POST'])
def add_scheduled_stream():
    data = request.json
    streamer_name = data.get("streamer_name")
    stream_title = data.get("stream_title")
    stream_description = data.get("stream_description")
    start_time = data.get("start_time")
    end_time = data.get("end_time")
    tags = data.get("tags")
    video_url = data.get("video_url")
    chapters = data.get("chapters")

    #TODO: Add validation for the input fields
    #TODO: Generate chapters for the video and store in the database

    scheduled_stream = {
        "streamer_name": streamer_name,
        "video_url": video_url,
        "stream_title": stream_title,
        "stream_description": stream_description,
        "start_time": start_time,
        "end_time": end_time,
        "tags": tags,
        "chapters": chapters,
    }

    scheduled_streams_collection = db["scheduled_streams"]
    scheduled_streams_collection.insert_one(scheduled_stream)

    return "Scheduled stream added successfully"

# Create an api route to get all scheduled streams
@app.route('/get_scheduled_streams', methods=['GET'])
def get_scheduled_streams():
    scheduled_streams_collection = db["scheduled_streams"]
    scheduled_streams = list(scheduled_streams_collection.find())

    return {"scheduled_streams": scheduled_streams}

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
