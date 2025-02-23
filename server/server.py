from flask import Flask, render_template
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

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
