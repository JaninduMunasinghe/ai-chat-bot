import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up model and chat session
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get chatbot response
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Streamlit app configuration
st.set_page_config(page_title="ChatBot")

st.title("🤖 MedJourney Q&A Chatbot")

# Sidebar for input
st.sidebar.header("User Input")
input = st.sidebar.chat_input("Enter your question", key="input")

# Reset chat history button
if st.sidebar.button("Reset Chat"):
    st.session_state['chat_history'] = []
    st.experimental_rerun()

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Process user input and get response
if input:  # Check if input is provided
    with st.spinner("Bot is typing..."):
        response = get_gemini_response(input)
        st.session_state['chat_history'].append(("You", input))
        for chunk in response:
            st.session_state['chat_history'].append(("Bot", chunk.text))

# Display chat history (reversed)
st.subheader("Chat History")
chat_history_box = st.empty()

# Chat display with custom styling
def display_message(role, text):
    if role == "You":
        st.markdown(f"""
        <div style="background-color:lightblue;padding:10px;border-radius:10px;margin-bottom:25px">
            <strong>{role}:</strong> {text}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background-color:#f0f0f5;padding:10px;border-radius:10px;margin-bottom:2px">
            <strong>{role}:</strong> {text}
        </div>
        """, unsafe_allow_html=True)

# Display messages in reverse order (newest first)
with chat_history_box.container():
    for role, text in reversed(st.session_state['chat_history']):
        display_message(role, text)
