import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure API Key
# Configure API Key
genai.configure(api_key=st.secrets["general"]["GEMINI_API_KEY"])

# Your existing code here...

# Create the model generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 150,
    "response_mime_type": "text/plain",
}

# Function to generate content
def generate_content(prompt):
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Error generating content: {e}"

# Custom styles
st.markdown("""
    <style>
    .main-title {
        font-size: 60px;
        color: #fafafa;
            
        font-family: 'Courier New', Courier, monospace;
        text-align: center;
        background-color: #328fa8;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .sticker {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# App Title with custom name and stickers
st.markdown("<div class='main-title'>🎮 StoryForge by Ahsan 🎨</div>", unsafe_allow_html=True)

# Add a custom sticker or logo
st.markdown("<div class='sticker'><img src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSky4r2FNd_KFBvqNfBpzaWX9vxQRRKn-NYhQ&s' width='100'></div>", unsafe_allow_html=True)

# App description
st.write("StoryForge helps game developers generate comprehensive Game Design Documents. Input details about your game environment, protagonist, and antagonist to create a structured design document.")

# Sidebar for user inputs
with st.sidebar:
    st.header("Game Details")
    game_environment = st.text_input("Game Environment", "Describe the setting of your game")
    protagonist = st.text_input("Protagonist", "Describe the main character")
    antagonist = st.text_input("Antagonist", "Describe the main villain or opposing force")

    if st.button("Generate Document"):
        env_description = generate_content(f"Create a detailed description of a game environment based on this input: {game_environment}")
        protagonist_description = generate_content(f"Create a detailed description of a game protagonist based on this input: {protagonist}")
        antagonist_description = generate_content(f"Create a detailed description of a game antagonist based on this input: {antagonist}")
        game_story = generate_content(f"Create a detailed game story based on the following inputs:\nGame Environment: {env_description}\nProtagonist: {protagonist_description}\nAntagonist: {antagonist_description}")

        st.session_state.env_description = env_description
        st.session_state.protagonist_description = protagonist_description
        st.session_state.antagonist_description = antagonist_description
        st.session_state.game_story = game_story

# Two-column layout for displaying content
col1, col2 = st.columns(2)

with col1:
    st.header("Game Environment")
    if 'env_description' in st.session_state:
        st.write(st.session_state.env_description)
    else:
        st.write("Waiting for input...")

with col2:
    st.header("Game Story")
    if 'game_story' in st.session_state:
        st.write(st.session_state.game_story)
    else:
        st.write("Your game story will be generated based on the inputs provided.")

with col1:
    st.header("Protagonist")
    if 'protagonist_description' in st.session_state:
        st.write(st.session_state.protagonist_description)
    else:
        st.write("Waiting for input...")

with col2:
    st.header("Antagonist")
    if 'antagonist_description' in st.session_state:
        st.write(st.session_state.antagonist_description)
    else:
        st.write("Waiting for input...")
