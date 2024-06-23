from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os
import uuid
import pandas as pd
import openai
from openai import OpenAI


# Knowledge Base (RAG System) Imports #
import nest_asyncio
nest_asyncio.apply()

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.core.memory import ChatMemoryBuffer
#------------------------------------#


# Google Sheets API Imports #
from google.oauth2 import service_account
from googleapiclient.discovery import build


#--------------------------------#

load_dotenv()


app = Flask(__name__)

CORS(app)  # enable CORS


OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()


# Prompt Engineering #
context = """You are a conversational AI bot designed to assist users with information about HackerEarth. Your role includes:
1. Answering questions about HackerEarth, its products, services, and mission.
2. Providing information about available demos and their benefits.
3. Prompting users to sign up for a demo or contact HackerEarth for more details.
4. Handling common user inquiries and offering assistance.

HackerEarth is a tech hiring platform that helps recruiters and engineering managers effortlessly hire the best developers thanks to a powerful suite of virtual recruiting tools that help identify, assess, interview and engage developers.

Use the provided information and sources to ensure your responses are accurate and helpful.
"""
#-------------------#


# Google Sheets Setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = './credentials.json'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = '1kZtPJnFcJ4YA9WPRhGqvoHMm8grE_n9v-rfnNkT5ZaY'
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()



# ----------------------------#

# Knowledge Base (RAG System) #
PERSIST_DIR = "./storage"

if not os.path.exists(PERSIST_DIR):
    documents = SimpleDirectoryReader("Knowledge_Base").load_data()
    index = VectorStoreIndex.from_documents(documents, show_progress=True)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

# query_engine = index.as_chat_engine()

# response = query_engine.query("What is HackerEarth?")
# print(response)

memory = ChatMemoryBuffer.from_defaults(token_limit=5000)
chat_engine = index.as_chat_engine(
    chat_mode="context",
    memory=memory,
    system_prompt=(
        context
    ),
)

# ----------------------------#


@app.route('/') 
def home():
    return jsonify({'message': 'Working!'})


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('prompt')
    conversation_state = data.get('conversation_state', 'initial')
    user_info = data.get('user_info', {})

    print(f"State: {conversation_state}")
    print(f"User info: {user_info}")

    if conversation_state == 'initial':
        response = chat_engine.chat(user_message)
        conversation_state = 'collect_info'
        return jsonify({'response': response.response + " Could you please provide your name, email, and company name?", 'conversation_state': conversation_state, 'user_info': user_info})

    elif conversation_state == 'collect_info':
        user_info = extract_user_info(user_message)
        conversation_state = 'completed'

        # Store the user info in Google Sheets
        store_user_info(user_info)
        
        return jsonify({'response': "Thank you for providing your details. How can I assist you further?", 'conversation_state': conversation_state, 'user_info': user_info})

    else:
        response = chat_engine.chat(user_message)
        return jsonify({'response': response.response, 'conversation_state': conversation_state, 'user_info': user_info})

def extract_user_info(user_message):
    # Use OpenAI's API to parse the user's input for name, email, and company
    prompt = f"Extract the following details from the user's message: {user_message}\n\nDetails to extract:\nName: \nEmail: \nCompany:"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "user", "content": prompt},
        ],
    )

    response_text = response.choices[0].message.content

    # Parse the response text to extract the details
    lines = response_text.split("\n")
    user_info = {}
    for line in lines:
        if "Name:" in line:
            user_info['name'] = line.split("Name:")[1].strip()
        elif "Email:" in line:
            user_info['email'] = line.split("Email:")[1].strip()
        elif "Company:" in line:
            user_info['company'] = line.split("Company:")[1].strip()

    return user_info

def store_user_info(user_info):
    values = [
        [user_info.get('name'), user_info.get('email'), user_info.get('company')]
    ]
    body = {
        'values': values
    }
    sheet.values().append(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range="Sheet1!A1:C1",
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
