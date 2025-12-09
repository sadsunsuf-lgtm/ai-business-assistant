import streamlit as st
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="centered"
)

# Initialize Groq client
@st.cache_resource
def load_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.7,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

llm = load_llm()

# App title and description
st.title("🤖 My AI Chat Assistant")
st.markdown("Chat with AI powered by Groq and Hugging Face models!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What would you like to know?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm.invoke(prompt)
            st.markdown(response.content)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.content})
