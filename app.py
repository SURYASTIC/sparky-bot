import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="My Website Bot", layout="centered")

# Retrieve API Key from Streamlit Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key is missing. Please set it in Streamlit Secrets.")
    st.stop()

# --- 2. MODEL SETUP ---
# We selected this specific model from your screenshot list:
model_name="gemini-pro-latest"

# PASTE YOUR CUSTOM KNOWLEDGE BELOW
system_instruction = """
You are a helpful customer support AI.
Answer strictly based on the text below. If the answer is not there, say you don't know.

--- START KNOWLEDGE BASE ---
[Paste your website text, FAQs, and pricing here...]
--- END KNOWLEDGE BASE ---
"""

try:
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_instruction
    )
except Exception as e:
    st.error(f"Error connecting to model: {e}")

# --- 3. CHAT INTERFACE ---
# Hide standard Streamlit elements to look like a widget
st.markdown("""
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("Chat with Us")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Send message to Google AI
        chat = model.start_chat(history=[
            {"role": m["role"], "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1]
        ])
        response = chat.send_message(prompt)
        
        st.session_state.messages.append({"role": "model", "content": response.text})
        with st.chat_message("model"):
            st.markdown(response.text)
            
    except Exception as e:
        # If the Lite model fails, show the specific error
        st.error(f"An error occurred: {e}")
