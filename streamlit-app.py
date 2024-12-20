import streamlit as st
import requests
from typing import List, Dict, Any, Optional

st.title("Market Mate")

# Hard coding a userid for now. This should be available after person logs in.
USER_ID: str = "nniishantkumar@gmail.com"


def create_conversation(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Create a new conversation for the given user.

    Args:
        user_id (str): The unique identifier for the user.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the new conversation info if successful, None otherwise.
    """
    response = requests.post(f"http://localhost:5000/users/{user_id}/conversations")
    if response.status_code == 201:
        return response.json()
    else:
        st.sidebar.error(
            f"Error: {response.json().get('error', 'Failed to create a new conversation.')}")
        return None


def fetch_conversations(user_id: str) -> List[Dict[str, Any]]:
    """
    Fetch all conversations for the given user.

    Args:
        user_id (str): The unique identifier for the user.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing conversation details.
    """
    response = requests.get(f"http://localhost:5000/users/{user_id}/conversations")
    if response.status_code == 200:
        return response.json()
    else:
        st.sidebar.error(
            f"Error: {response.json().get('error', 'Failed to fetch conversations.')}")
        return []

if st.sidebar.button("Add New Conversation"):
    new_conversation_info = create_conversation(USER_ID)
    if new_conversation_info:
        st.sidebar.success("New conversation created")
        st.session_state.selected_conversation = new_conversation_info

conversations: List[Dict[str, Any]] = fetch_conversations(USER_ID)
st.sidebar.title("Conversations")
for conversation in conversations:
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        if st.button(conversation['conversation_name'], key=conversation['conversation_id']):
            st.session_state.selected_conversation = conversation
    with col2:
        if st.button("🗑️", key=f"delete_{conversation['conversation_id']}"):
            response = requests.delete(f"http://localhost:5000/conversations/{conversation['conversation_id']}")
            if response.status_code == 200:
                st.sidebar.success(f"Conversation {conversation['conversation_name']} deleted.")
                if "selected_conversation" in st.session_state and st.session_state.selected_conversation and st.session_state.selected_conversation['conversation_id'] == conversation['conversation_id']:
                    st.session_state.selected_conversation = None
                st.rerun()
            else:
                st.sidebar.error(
                    f"Error: {response.json().get('error', 'Failed to delete conversation.')}")


def fetch_messages(conversation_id: str) -> List[Dict[str, Any]]:
    """
    Fetch messages for a specific conversation.

    Args:
        conversation_id (str): The unique identifier for the conversation.

    Returns:
        List[Dict[str, Any]]: A list of messages filtered to include only user and assistant roles.
    """
    response = requests.get(f"http://localhost:5000/conversations/{conversation_id}")
    if response.status_code == 200:
        messages = response.json().get("messages", [])
        return [msg for msg in messages if msg["role"] in ["user", "assistant"] and msg["content"]]
    else:
        st.error(
            f"Error: {response.json().get('error', 'Failed to fetch messages.')}")
        return []

if "selected_conversation" in st.session_state and st.session_state.selected_conversation:
    st.session_state.messages = fetch_messages(st.session_state.selected_conversation['conversation_id'])
    st.title(st.session_state.selected_conversation['conversation_name'])
else:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if "selected_conversation" in st.session_state:
        response = requests.post(
            f"http://localhost:5000/users/{USER_ID}/conversations/{st.session_state.selected_conversation['conversation_id']}/send_message",
            json={"message": prompt}
        )
        if response.status_code == 200:
            ai_response = response.json()
            st.session_state.messages.append(ai_response)
            with st.chat_message(ai_response["role"]):
                st.markdown(ai_response["content"])
        else:
            st.error(
                f"Error: {response.json().get('error', 'Failed to send message.')}")
    else:
        st.error("No conversation selected.")