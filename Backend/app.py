from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
import requests
from dotenv import load_dotenv
import os
import uuid
import pandas as pd
import openai
from openai import OpenAI
from datetime import datetime
import pytz # For timezone conversion


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


app = Flask(__name__, static_folder = '../Frontend/dist')

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

Please limit answers to around 65 words or less. If you need more information, ask the user for clarification or provide a general response.
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



@app.route('/chat', methods=['POST'])
@cross_origin()
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
        return jsonify({'response': response.response + "\n" + "\n" + "\n" + "Could you please provide your name, email, and company name?", 'conversation_state': conversation_state, 'user_info': user_info})

    elif conversation_state == 'collect_info':
        user_info, info_found = extract_user_info(user_message)
        conversation_state = 'completed'
        if info_found:
            store_user_info(user_info)
            return jsonify({'response': "Thank you for providing your details. How can I assist you further?", 'conversation_state': conversation_state, 'user_info': user_info})
        else:
            # User did not provide contact info, answer their question instead
            response = chat_engine.chat(user_message)
            return jsonify({'response': response.response, 'conversation_state': conversation_state, 'user_info': user_info})
    
    else:
        response = chat_engine.chat(user_message)
        return jsonify({'response': response.response, 'conversation_state': conversation_state, 'user_info': user_info})

def extract_user_info(user_message):
    prompt = f"Extract the following details from the user's message: {user_message}\n\nDetails to extract:\nName: \nEmail: \nCompany: \n\n If they didn't provide anything or asked a question then populate a value called InfoProvided: and put False in it."


    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "user", "content": prompt},
        ],
    )


    response_text = response.choices[0].message.content
    user_info = {}
    info_found = False

    lines = response_text.split("\n")
    for line in lines:
        if "Name:" in line:
            name = line.split("Name:")[1].strip()
            if name:
                user_info['name'] = name
                info_found = True
        if "Email:" in line:
            email = line.split("Email:")[1].strip()
            if email:
                user_info['email'] = email
                info_found = True
        if "Company:" in line:
            company = line.split("Company:")[1].strip()
            if company:
                user_info['company'] = company
                info_found = True
        if "InfoProvided:" in line:
            info_provided = line.split("InfoProvided:")[1].strip()
            if info_provided == "False":
                info_found = False


    return user_info, info_found

def store_user_info(user_info):
    pst_timezone = pytz.timezone('America/Los_Angeles')
    current_time_pst = datetime.now(pst_timezone).strftime('%Y-%m-%d %H:%M:%S')

    values = [
        [user_info.get('name'), user_info.get('email'), user_info.get('company'), current_time_pst]
    ]
    body = {
        'values': values
    }
    sheet.values().append(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range="Sheet1!A:D",
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()

@app.route('/')
@cross_origin()
def server():
    return send_from_directory('../Frontend/dist', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
