import gradio as gr
import requests

# Define the chat endpoint
CHAT_ENDPOINT = "http://127.0.0.1:8080/chat"

# Initialize session ID globally
session_id = None

def chat_with_ai(user_input, chat_history):
    global session_id
    
    payload = {
        "session_id": session_id,
        "question": user_input
    }
    
    try:
        response = requests.post(CHAT_ENDPOINT, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            session_id = result.get("session_id")
            ai_response = result.get("answer")
            
            chat_history.append((user_input, ai_response))
            return chat_history, ""
        else:
            return chat_history, f"Error {response.status_code}: {response.json().get('detail', 'Unknown error')}"
    except Exception as e:
        return chat_history, f"An error occurred: {str(e)}"

def reset_chat():
    global session_id
    session_id = None
    return None, "Chat reset. How can I help you?"

# Custom CSS for a full-screen, dark theme interface with original button layout
custom_css = """
/* Full-screen dark theme layout */
body, .gradio-container, #component-0 {
    background-color: #1a1a1a;
    margin: 0;
    padding: 0;
    height: 100vh;
    max-height: 100vh;
    overflow: hidden;
}

/* Chat container settings */
.contain {
    background-color: #2a2a2a;
    border-radius: 0;
    padding: 0;
    margin: 0;
    height: 100vh;
    max-height: 100vh;
    display: flex;
    flex-direction: column;
}

/* Header text settings */
.header-text {
    background-color: #2a2a2a;
    color: #e5e5e5;
    padding: 1rem;
    margin: 0;
    font-size: 1.5rem;
    font-weight: bold;
    text-align: center;
    letter-spacing: 0.5px;
}

/* Chatbot area */
#chatbot {
    flex-grow: 1;
    overflow-y: auto;
    padding: 1rem;
    background-color: #1e1e1e;
    border-top: 1px solid #333;
}

/* Message settings */
#chatbot .message {
    padding: 12px 15px;
    margin: 10px 0;
    border-radius: 8px;
    max-width: 80%;
    font-family: 'Arial', sans-serif;
    font-size: 1rem;
    line-height: 1.5;
    word-wrap: break-word;
    transition: background-color 0.3s ease-in-out;
}

/* User messages */
#chatbot .user {
    background-color: #2b5797;
    color: white;
    margin-left: auto;
    text-align: right;
}

/* Bot/Assistant messages */
#chatbot .bot {
    background-color: #444;
    color: #e5e5e5;
    text-align: left;
}

/* Input area */
.input-container {
    padding: 1rem;
    background-color: #2a2a2a;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    border-top: 1px solid #333;
}

/* Input box */
#component-2 {
    background-color: #3a3a3a;
    border: none;
    color: white;
    margin-bottom: 0.5rem;
    padding: 10px 15px;
    width: 85%;
    font-size: 1rem;
    border-radius: 8px;
    outline: none;
    box-shadow: none;
    transition: background-color 0.3s ease-in-out;
}

#component-2:focus {
    background-color: #4a4a4a;
}

/* Submit button */
#component-3, #component-4 {
    background-color: #4a5568;
    color: white;
    border: none;
    padding: 10px 20px;
    font-size: 1rem;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease-in-out;
}

#component-3:hover, #component-4:hover {
    background-color: #2b5797;
}

/* Scrollbar customization */
#chatbot::-webkit-scrollbar {
    width: 8px;
}

#chatbot::-webkit-scrollbar-thumb {
    background-color: #444;
    border-radius: 8px;
}

"""

with gr.Blocks(css=custom_css) as demo:
    gr.HTML('<div class="header-text">Chat with MONEYME AI</div>')
    
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
        height=600,  # This height will be overridden by CSS
    )
    
    with gr.Column(elem_classes="input-container"):
        msg = gr.Textbox(
            show_label=False,
            placeholder="Type your message here...",
        )
        with gr.Row():
            submit_btn = gr.Button("Send")
            reset_btn = gr.Button("Reset Chat")

    submit_btn.click(chat_with_ai, inputs=[msg, chatbot], outputs=[chatbot, msg])
    reset_btn.click(reset_chat, outputs=[chatbot, msg])

if __name__ == "__main__":
    demo.launch()