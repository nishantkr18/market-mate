from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB Setup
client = MongoClient('mongodb://localhost:27017/')
db = client['marketmate']
users_collection = db['users']
conversations_collection = db['conversations']

def get_user_conversations(user_id):
    """
    Get all conversations for a user. 
    Returns a reversed list of objects, each containing conversation_id and conversation_name.
    """
    user = users_collection.find_one({"user_id": user_id})
    if not user:
        return None
    return list(reversed(user["conversations"]))

def get_conversation(conversation_id):
    """
    Get an entire conversation given a conversation_id.
    Returns the conversation details including all messages.
    """
    conversation = conversations_collection.find_one({"_id": ObjectId(conversation_id)})
    if not conversation:
        return None
    # Convert ObjectId to string for JSON serialization
    conversation["_id"] = str(conversation["_id"])
    return conversation

def create_user_conversation(user_id):
    """
    Create a new conversation for a user.
    Returns a conversation_id and adds the conversation to the user.
    """
    user = users_collection.find_one({"user_id": user_id})
    if not user:
        return None

    conversation_count = len(user.get("conversations", []))
    new_conversation_name = f"Conversation {conversation_count + 1}"

    new_conversation = {
        "conversation_name": new_conversation_name,
        "messages": []  # Initialize with an empty message list
    }
    conversation_id = conversations_collection.insert_one(new_conversation).inserted_id
    conversation_info = {"conversation_id": str(
        conversation_id), "conversation_name": new_conversation_name}

    users_collection.update_one(
        {"user_id": user_id},
        {"$push": {"conversations": conversation_info}},
        upsert=True
    )

    return conversation_info


def delete_conversation(conversation_id):
    """
    Delete a specific conversation.
    """
    conversation = conversations_collection.find_one({"_id": ObjectId(conversation_id)})
    if not conversation:
        return False

    conversations_collection.delete_one({"_id": ObjectId(conversation_id)})

    users_collection.update_one(
        {"conversations.conversation_id": conversation_id},
        {"$pull": {"conversations": {"conversation_id": conversation_id}}}
    )

    return True


def update_conversation_history(conversation_id, messages):
    """
    Update the conversation history with new messages.
    """
    conversations_collection.update_one(
        {"_id": ObjectId(conversation_id)},
        {"$set": {"messages": messages}}
    )
