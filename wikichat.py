import streamlit as st
import wikipedia

# Title
st.title("🧠 Simple Python Chatbot with Wikipedia")

# Session state for conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Define your bot's logic
def chatbot_response(user_input):
    user_input = user_input.lower()
    
    # Basic rule-based responses
    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you today?"
    elif "your name" in user_input:
        return "I'm a Streamlit Chatbot created in Python!"
    elif "bye" in user_input:
        return "Goodbye! Have a great day."
    else:
        # Try Wikipedia if no rule-based response
        try:
            summary = wikipedia.summary(user_input, sentences=2)
            return f"📖 From Wikipedia:\n\n{summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"⚠️ That query is too broad. Did you mean: {', '.join(e.options[:5])}?"
        except wikipedia.exceptions.PageError:
            return "❌ Sorry, I couldn't find anything on Wikipedia for that."
        except Exception as e:
            return f"⚠️ An error occurred: {e}"

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get bot response
    response = chatbot_response(user_input)
    st.session_state.messages.append({"role": "bot", "content": response})

# Display conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
