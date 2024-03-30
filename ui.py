import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_host = os.environ.get("HOST", "localhost")
api_port = int(os.environ.get("PORT", 8501))

# Streamlit UI elements
st.title("Mental Health Companion")

question = st.text_input(
    "Ask for support or advice",
    placeholder="How can I help you today?"
)

if question:
    url = f'http://{api_host}:{api_port}/query'
    data = {"query": question}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        st.write("### Response")
        st.write(response.json()["result"])
    else:
        st.error(f"Failed to send data to the backend. Status code: {response.status_code}")