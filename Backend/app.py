from flask import Flask, request, jsonify, session
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os
import uuid
import pandas as pd


# Knowledge Base (RAG System) Imports #
import nest_asyncio
nest_asyncio.apply()

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
#------------------------------------#

load_dotenv()

app = Flask(__name__)
CORS(app)  # enable CORS

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


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

# Knowledge Base (RAG System) #
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY


PERSIST_DIR = "./storage"

if not os.path.exists(PERSIST_DIR):
    documents = SimpleDirectoryReader("Knowledge_Base").load_data()
    index = VectorStoreIndex.from_documents(documents, show_progress=True)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

query_engine = index.as_chat_engine()

# response = query_engine.query("What is HackerEarth?")
# print(response)


# ----------------------------#



@app.route('/') 
def home():
    return jsonify({'message': 'Working!'})


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('prompt')

    # headers = {
    #     'Authorization': f'Bearer ' + OPENAI_API_KEY,
    #     'Content-Type': 'application/json',
    # }
    # json_data = {
    #     'model': 'gpt-3.5-turbo',
    #     'messages': [
    #         {'role': 'system', 'content': context},
    #         {'role': 'user', 'content': user_message}
    #     ],
    #     'temperature': 0.7,
    # }

    # response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)

    # if response.status_code != 200:
    #     return jsonify({'error': 'Failed to get response from OpenAI API', 'status_code': response.status_code, 'details': response.text}), 500

    # response_json = response.json()

    # if 'choices' not in response_json:
    #     return jsonify({'error': 'Invalid response format from OpenAI API', 'response': response_json}), 500

    # response_text = response_json['choices'][0]['message']['content'].strip()


    response = query_engine.query(user_message)

    return jsonify({'response': response.response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
