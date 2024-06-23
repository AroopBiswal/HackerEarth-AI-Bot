from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)  # enable CORS

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('prompt')

    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    headers = {
        'Authorization': f'Bearer ' + OPENAI_API_KEY,
        'Content-Type': 'application/json',
    }
    json_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': user_message}],
        'temperature': 0.7,
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to get response from OpenAI API', 'status_code': response.status_code, 'details': response.text}), 500

    response_json = response.json()

    if 'choices' not in response_json:
        return jsonify({'error': 'Invalid response format from OpenAI API', 'response': response_json}), 500

    response_text = response_json['choices'][0]['message']['content'].strip()

    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
