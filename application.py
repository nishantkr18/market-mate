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
from typing import Any, Dict, Optional

# Initialize the Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key'

# Initialize Extensions
CORS(app)

# Routes
@app.route('/')
def home() -> Any:
    """
    Home route for the application.

    Returns:
        Response: A JSON response with a welcome message.
    """
    return jsonify({"message": "Welcome to MarketMate!"})

@app.route('/users/<user_id>/conversations', methods=['GET'])
def get_user_conversations_route(user_id: str) -> Any:
    """
    Get all conversations for a user.

    Args:
        user_id (str): The unique identifier for the user.

    Returns:
        Response: A JSON response containing a list of conversations or an error message.
    """
    conversations = get_user_conversations(user_id)
    if conversations is None:
        return jsonify({"error": "User not found."}), 404
    
    return jsonify(conversations), 200

@app.route('/conversations/<conversation_id>', methods=['GET'])
def get_conversation_route(conversation_id: str) -> Any:
    """
    Get an entire conversation given a conversation_id.

    Args:
        conversation_id (str): The unique identifier for the conversation.

    Returns:
        Response: A JSON response containing the conversation details or an error message.
    """
    conversation = get_conversation(conversation_id)
    if conversation is None:
        return jsonify({"error": "Conversation not found."}), 404

    return jsonify(conversation), 200

@app.route('/users/<user_id>/conversations', methods=['POST'])
def create_user_conversation_route(user_id: str) -> Any:
    """
    Create a new conversation for a user.

    Args:
        user_id (str): The unique identifier for the user.

    Returns:
        Response: A JSON response containing the new conversation info or an error message.
    """
    conversation_info = create_user_conversation(user_id)
    if conversation_info is None:
        return jsonify({"error": "User not found."}), 404

    return jsonify(conversation_info), 201

@app.route('/users/<user_id>/conversations/<conversation_id>/send_message', methods=['POST'])
@request_rate_limit()
def send_message_to_conversation_route(user_id: str, conversation_id: str) -> Any:
    """
    Send a message to a specific conversation.

    Args:
        user_id (str): The unique identifier for the user.
        conversation_id (str): The unique identifier for the conversation.

    Returns:
        Response: A JSON response containing the AI's response or an error message.
    """
    data: Optional[Dict[str, Any]] = request.get_json()
    user_message: Optional[str] = data.get("message") if data else None

    if not user_message:
        return jsonify({"error": "Message content is required."}), 400

    ai_response = get_answer_in_conversation(conversation_id, user_message)
    if ai_response is None:
        return jsonify({"error": "Conversation not found."}), 404

    return jsonify(ai_response), 200

@app.route('/conversations/<conversation_id>', methods=['DELETE'])
def delete_conversation_route(conversation_id: str) -> Any:
    """
    Delete a specific conversation.

    Args:
        conversation_id (str): The unique identifier for the conversation.

    Returns:
        Response: A JSON response indicating success or failure.
    """
    success = delete_conversation(conversation_id)
    if not success:
        return jsonify({"error": "Conversation not found."}), 404

    return jsonify({"message": "Conversation deleted successfully."}), 200

if __name__ == '__main__':
    app.run(debug=True)
