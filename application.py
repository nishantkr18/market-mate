from flask import Flask, jsonify, request
from flask_cors import CORS
from src.rate_limiter import request_rate_limit
from src.agent import get_answer_in_conversation
from src.database import (
    get_user_conversations,
    get_conversation,
    create_user_conversation,
    delete_conversation
)

# Initialize the Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key'

# Initialize Extensions
CORS(app)

# Routes
@app.route('/')
def home():
    return jsonify({"message": "Welcome to MarketMate!"})

@app.route('/users/<user_id>/conversations', methods=['GET'])
def get_user_conversations_route(user_id):
    """
    Get all conversations for a user. 
    Returns a reversed list of objects, each containing conversation_id and conversation_name.
    """
    conversations = get_user_conversations(user_id)
    if conversations is None:
        return jsonify({"error": "User not found."}), 404
    
    return jsonify(conversations), 200

@app.route('/conversations/<conversation_id>', methods=['GET'])
def get_conversation_route(conversation_id):
    """
    Get an entire conversation given a conversation_id.
    Returns the conversation details including all messages.
    """
    conversation = get_conversation(conversation_id)
    if conversation is None:
        return jsonify({"error": "Conversation not found."}), 404

    return jsonify(conversation), 200

@app.route('/users/<user_id>/conversations', methods=['POST'])
def create_user_conversation_route(user_id):
    """
    Create a new conversation for a user.
    Returns a conversation_id and adds the conversation to the user.
    """
    conversation_info = create_user_conversation(user_id)
    if conversation_info is None:
        return jsonify({"error": "User not found."}), 404

    return jsonify(conversation_info), 201


@app.route('/users/<user_id>/conversations/<conversation_id>/send_message', methods=['POST'])
@request_rate_limit()
def send_message_to_conversation_route(user_id, conversation_id):
    """
    Send a message to a specific conversation.
    Returns only the AI response to the user's message.
    """
    data = request.get_json()
    user_message = data.get("message")

    ai_response = get_answer_in_conversation(conversation_id, user_message)
    if ai_response is None:
        return jsonify({"error": "Conversation not found."}), 404

    return jsonify(ai_response), 200

@app.route('/conversations/<conversation_id>', methods=['DELETE'])
def delete_conversation_route(conversation_id):
    """
    Delete a specific conversation.
    """
    success = delete_conversation(conversation_id)
    if not success:
        return jsonify({"error": "Conversation not found."}), 404

    return jsonify({"message": "Conversation deleted successfully."}), 200

if __name__ == '__main__':
    app.run(debug=True)
