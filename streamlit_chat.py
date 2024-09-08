import streamlit as st
import requests
import time

# Define the chat endpoint
CHAT_ENDPOINT = "http://127.0.0.1:8080/chat"

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

def chat_with_ai(user_input):
    payload = {
        "session_id": st.session_state.session_id,
        "question": user_input
    }
    
    try:
        response = requests.post(CHAT_ENDPOINT, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            st.session_state.session_id = result.get("session_id")
            return result.get("answer")
        else:
            return f"Error {response.status_code}: {response.json().get('detail', 'Unknown error')}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def reset_chat():
    st.session_state.session_id = None
    st.session_state.messages = []
    # Clear session state and reset the page without full rerun
    st.experimental_set_query_params(reset="true")
    st.experimental_set_query_params(reset="")

# App layout
st.title("Chat with MONEYME AI")

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = chat_with_ai(prompt)
        
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Reset chat button (placed in the sidebar)
with st.sidebar:
    if st.button("RESET CHAT", key="reset_button"):
        reset_chat()
