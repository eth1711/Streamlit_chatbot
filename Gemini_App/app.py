import streamlit as st
import google.generativeai as genai

# Configure Gemini API
GOOGLE_API_KEY = st.secrets["API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def get_gemini_response(prompt):
    # Build the conversation history as context with the last 5 messages
    conversation_history = ""
    for message in st.session_state.messages[-5:]:  # Only use the last 5 messages
        conversation_history += f"{message['role']}: {message['content']}\n"
    
    # Append the new prompt to the history
    conversation_history += f"user: {prompt}\n"

    # Use the conversation history as the full prompt for Gemini
    response = model.generate_content(conversation_history)
    return response.text

def main():
    st.title("Gemini AI Chatbot")
    
    initialize_session_state()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Chat with Gemini"):
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get Gemini response
        response = get_gemini_response(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.write(response)
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
