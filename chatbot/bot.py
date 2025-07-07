from flask import Flask, request
import requests
import os

app = Flask(__name__)

API_URL = os.getenv("API_URL")

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = requests.post(f"{API_URL}/api/chat", json={"message": user_message})
    return response.json()

if __name__ == '__main__':
    app.run(port=5001)