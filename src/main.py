import streamlit as st
import google.generativeai as genai
import base64

# Load API key from Streamlit Secrets
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("🚨 Gemini API key is missing in Streamlit secrets!")
    st.stop()

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Streamlit page settings
st.set_page_config(
    page_title="CyberSh@rk ChatGPT",
    page_icon="💬",
    layout="wide"
)

# Function to set background image with slight contrast reduction
def set_background(image_path):
    with open(image_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()

    background_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        opacity: 0.92;
        filter: brightness(0.92) contrast(0.88);
    }}

    .title-container {{
        position: relative;
        top: 0px;
        left: 20px;
        color: white !important;
        font-size: 28px;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        text-shadow: 2px 2px 4px black;
        padding: 10px 0;
    }}

    .chat-container {{
        margin-top: 50px;
        padding: 10px;
    }}

    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    </style>
    """
    st.markdown(background_css, unsafe_allow_html=True)

# Call function to set background
set_background("src/Corrupted.jpg")  # Change path as needed

# Title with shadow effect to create a bordered appearance
st.markdown('<div class="title-container">🤖 CyberSh@rk Bot</div>', unsafe_allow_html=True)

# Chat UI container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# CSS for message alignment
chat_css = """
<style>
.user-message {
    background-color: #1E1E2F;
    color: white;
    border-radius: 15px;
    padding: 10px;
    margin: 5px;
    text-align: right;
    width: fit-content;
    max-width: 70%;
    margin-left: auto;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.4);
}

.assistant-message {
    background-color: white;
    color: black;
    border-radius: 15px;
    padding: 10px;
    margin: 5px;
    text-align: left;
    width: fit-content;
    max-width: 70%;
    margin-right: auto;
    border: 1px solid #ddd;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
}

.loading-message {
    background-color: white;
    color: black;
    border-radius: 15px;
    padding: 10px;
    margin: 5px;
    text-align: left;
    width: fit-content;
    max-width: 70%;
    margin-right: auto;
    border: 1px solid #ddd;
    font-style: italic;
    opacity: 0.7;
}
</style>
"""
st.markdown(chat_css, unsafe_allow_html=True)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    role = message["role"]
    content = message["content"]

    if role == "user":
        st.markdown(f'<div class="user-message">{content}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{content}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# User input field
user_prompt = st.chat_input("Ask Anything..")

if user_prompt:
    # Add user's message to chat
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    st.markdown(f'<div class="user-message">{user_prompt}</div>', unsafe_allow_html=True)

    # Placeholder for "Generating..." message
    placeholder = st.empty()

    try:
        # Display loading message
        with placeholder:
            st.markdown('<div class="loading-message">Generating...</div>', unsafe_allow_html=True)

        # Call Gemini API
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(user_prompt)

        assistant_response = response.text
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

        # Replace placeholder with actual response
        placeholder.empty()
        st.markdown(f'<div class="assistant-message">{assistant_response}</div>', unsafe_allow_html=True)

    except Exception as e:
        placeholder.empty()
        st.error(f"🚨 Unexpected error: {e}")
