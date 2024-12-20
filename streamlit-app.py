import streamlit as st
import requests
st.title("ChatGPT-like clone")

USER_ID = "nniishantkumar@gmail.com"

# Function to create a new conversation
def create_conversation(user_id):
    response = requests.post(f"http://localhost:5000/users/{user_id}/conversations")
    if response.status_code == 201:
        return response.json()
    else:
        return None

# Fetch user conversations and display in sidebar
def fetch_conversations(user_id):
    response = requests.get(f"http://localhost:5000/users/{user_id}/conversations")
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Add button to create a new conversation
if st.sidebar.button("Add New Conversation"):
    new_conversation_info = create_conversation(USER_ID)
    if new_conversation_info:
        st.sidebar.success(f"New conversation created")
        # Select the new conversation
        st.session_state.selected_conversation = new_conversation_info
    else:
        st.sidebar.error("Failed to create a new conversation.")

conversations = fetch_conversations(USER_ID)
st.sidebar.title("Conversations")
for conversation in conversations:
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        if st.button(conversation['conversation_name'], key=conversation['conversation_id']):
            st.session_state.selected_conversation = conversation
    with col2:
        if st.button("🗑️", key=f"delete_{conversation['conversation_id']}"):
            # Add logic to delete the conversation
            response = requests.delete(f"http://localhost:5000/conversations/{conversation['conversation_id']}")
            if response.status_code == 200:
                st.sidebar.success(f"Conversation {conversation['conversation_name']} deleted.")
                if "selected_conversation" in st.session_state and st.session_state.selected_conversation and st.session_state.selected_conversation['conversation_id'] == conversation['conversation_id']:
                    st.session_state.selected_conversation = None
                st.rerun()
            else:
                st.sidebar.error("Failed to delete conversation.")

# Fetch messages for the selected conversation
def fetch_messages(conversation_id):
    response = requests.get(f"http://localhost:5000/conversations/{conversation_id}")
    if response.status_code == 200:
        messages = response.json().get("messages", [])
        # Filter to only return human and AI responses
        return [msg for msg in messages if msg["role"] in ["user", "assistant"] and msg["content"]]
    else:
        return []

# Display messages for the selected conversation
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

    # Send the user's message to the conversation
    if "selected_conversation" in st.session_state:
        response = requests.post(
            f"http://localhost:5000/conversations/{st.session_state.selected_conversation['conversation_id']}/send_message",
            json={"message": prompt}
        )
        if response.status_code == 200:
            ai_response = response.json()
            st.session_state.messages.append(ai_response)
            with st.chat_message(ai_response["role"]):
                st.markdown(ai_response["content"])
        else:
            st.error("Failed to send message.")
    else:
        st.error("No conversation selected.")