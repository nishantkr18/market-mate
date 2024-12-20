from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB Setup
client = MongoClient('mongodb://localhost:27017/')
db = client['marketmate']
users_collection = db['users']
conversations_collection = db['conversations']

def get_user_conversations(user_id):
    """
    Retrieve all conversations associated with a specific user.

    Args:
        user_id (str): The unique identifier for the user.

    Returns:
        list: A reversed list of dictionaries, each containing 'conversation_id' and 'conversation_name'.
              Returns None if the user is not found.
    """
    user = users_collection.find_one({"user_id": user_id})
    if not user:
        return None
    return list(reversed(user["conversations"]))

def get_conversation(conversation_id):
    """
    Retrieve the details of a specific conversation using its ID.

    Args:
        conversation_id (str): The unique identifier for the conversation.

    Returns:
        dict: A dictionary containing the conversation details, including all messages.
              The '_id' field is converted to a string for JSON serialization.
              Returns None if the conversation is not found.
    """
    conversation = conversations_collection.find_one({"_id": ObjectId(conversation_id)})
    if not conversation:
        return None
    # Convert ObjectId to string for JSON serialization
    conversation["_id"] = str(conversation["_id"])
    return conversation

def create_user_conversation(user_id):
    """
    Create a new conversation for a user and add it to their list of conversations.

    Args:
        user_id (str): The unique identifier for the user.

    Returns:
        dict: A dictionary containing 'conversation_id' and 'conversation_name' of the newly created conversation.
              Returns None if the user is not found.
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
    Delete a specific conversation from the database.

    Args:
        conversation_id (str): The unique identifier for the conversation to be deleted.

    Returns:
        bool: True if the conversation was successfully deleted, False if the conversation was not found.
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
    Update the message history of a specific conversation.

    Args:
        conversation_id (str): The unique identifier for the conversation.
        messages (list): A list of messages to update the conversation with.

    Returns:
        None
    """
    conversations_collection.update_one(
        {"_id": ObjectId(conversation_id)},
        {"$set": {"messages": messages}}
    )
