from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import db_op as db

load_dotenv()
PASSWORD = os.getenv('PASSWORD')

app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'Hello there!\n', 200

@app.route('/add-chat', methods=['POST'])
def add_chat():
    data = request.get_json()
    if db.chat_exists(data['chat']):
        return 'Chat already exists', 409
    else:
        if data['password']==PASSWORD:
            return db.add_chat(data['chat'])
        else:
            return 'Unauthorized', 401

@app.route('/exists/<chat_id>', methods=['GET'])
def exists(chat_id):
    if db.chat_exists(chat_id):
        return 'Chat exists', 200
    else:
        return 'Chat does not exist', 404

if __name__ == "__main__":
    app.run(debug=True, host="192.168.100.61")