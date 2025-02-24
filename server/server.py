from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime
import pymongo
from pymongo import MongoClient
from flask_cors import CORS
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
import json
from bson import ObjectId

import requests
import os
import re
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import List, Dict
import hashlib
# from pinecone import Pinecone
import sys
from tqdm import tqdm



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

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")
def generate_llm_response(query: str, streamer_name: str, stream_title: str) -> str:
    # context_string = " ".join(doc['metadata']['text'] for doc in context['matches'])
    prompt_template = (
        "Context: Your name is {streamer_name} You are the host of a stream, in the middle of doing {stream_title}\n"
        "{query}\n"
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4", openai_api_key=OPENAI_API_KEY)
    prompt = PromptTemplate(input_variables=["query", "stream_title", "streamer_name"], template=prompt_template)
    chain = LLMChain(llm=llm, prompt=prompt)

    try:
        response = chain.run(query=query, stream_title=stream_title, streamer_name=streamer_name)
        return response
    except Exception as e:
        return f"Error generating LLM response: {str(e)}"

# This is a sample route to check if server is running
@app.route('/')
def index():
    return "Flask server is running!"


#simple api for client to tell server they joined a stream
@app.route('/join_stream', methods=['POST'])
def join_stream():
    data = request.json
    print("FUCK")
    print(data)
    username = data.get("username")
    streamer_name = data.get("streamer_name")
    stream_title = data.get("stream_title")
    print(f"User joined stream {username}")
    message = generate_llm_response(f"Greet the user {username} who just joined the stream, help them join in what you are doing", streamer_name=streamer_name, stream_title=stream_title)
    handle_send_message({"streamer_name": streamer_name, "stream_title": stream_title,"username": streamer_name, "message": message, "usernameColor": "#a83232"})
    return "User joined stream!"

# SocketIO event to handle sending and receiving messages
@socketio.on('send_message')
def handle_send_message(data):
    print(f"Received message from {data['username']}: {data['message']}")
    print(data)
    # Save message to MongoDB
    message = {
        "streamer_name": data['streamer_name'],
        "stream_title": data['stream_title'],
        "username": data['username'],
        "message": data['message'],
        "usernameColor": data['usernameColor'],
        "timestamp": datetime.now().isoformat()
    }
    messages_collection.insert_one(message)
    print(message)
    message["_id"] = str(message["_id"])
    # message.pop('timestamp', None)

    # Emit the message to all connected clients in real-time
    print("Emitting message to all clients..." + json.dumps(message))
    emit('receive_message', json.dumps(message), namespace='/', broadcast=True)

    # Get the amount of messages sent so far
    message_count = messages_collection.count_documents({})
    # If the message count % 3 == 0, send a message from the bot responding to the last message
    if message_count % 3 == 0:
        last_message = messages_collection.find().sort("timestamp", pymongo.DESCENDING).limit(1)[0]
        l_str = str(last_message["message"])
        streamer_name = last_message["streamer_name"]
        stream_title = last_message["stream_title"]
        bot_message = generate_llm_response(f"Respond to this message in a casual 1-2 sentence response: {l_str}", streamer_name=streamer_name, stream_title=stream_title)
        print(f"Bot message: {bot_message}")
        emit('receive_message', json.dumps({"streamer_name": streamer_name, "stream_title": stream_title, "username": streamer_name, "message": bot_message, "usernameColor": "#a83232"}), namespace='/', broadcast=True)
    

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
    for stream in scheduled_streams:
        stream["_id"] = str(stream["_id"])

    return {"scheduled_streams": scheduled_streams}

# Create an api route to get a scheduled stream by id
@app.route('/get_scheduled_stream/<stream_id>', methods=['GET'])
def get_scheduled_stream(stream_id):
    scheduled_streams_collection = db["scheduled_streams"]
    scheduled_stream = scheduled_streams_collection.find_one({"_id": ObjectId(stream_id)})
    

    if not scheduled_stream:
            return jsonify({"error": "Stream not found"}), 404
        
    # Convert ObjectId back to string for JSON serialization
    scheduled_stream["_id"] = str(scheduled_stream["_id"])
    
    return jsonify(scheduled_stream)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
