import streamlit as st
import wikipedia
try:
    from streamlit_mic_recorder import mic_recorder, speech_to_text
    MIC_AVAILABLE = True
except Exception:
    MIC_AVAILABLE = False

# Title
st.title("🧠 Simple Python Chatbot with Wikipedia")

# Session state for conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_input" not in st.session_state:
    st.session_state.pending_input = ""

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

# User input area with mic + text + send
user_input = None

with st.container():
    col_mic, col_text, col_send = st.columns([1, 8, 1])

    # Mic button (optional dependency)
    with col_mic:
        recognized_text = None
        if MIC_AVAILABLE:
            audio = mic_recorder(
                start_prompt="🎤",
                stop_prompt="⏹️",
                just_once=True,
                use_container_width=True,
                key="mic_recorder",
            )
            if audio and audio.get("bytes"):
                try:
                    recognized_text = speech_to_text(audio["bytes"]) or ""
                except Exception as e:
                    st.info(f"Speech recognition error: {e}")
        else:
            st.caption("Install 'streamlit-mic-recorder' to enable the mic")

        if recognized_text:
            st.session_state.pending_input = recognized_text.strip()

    with col_text:
        with st.form("chat_form", clear_on_submit=True):
            text_val = st.text_input(
                "Type your message...",
                value=st.session_state.get("pending_input", ""),
                label_visibility="collapsed",
                key="chat_text_input",
            )
            submitted = st.form_submit_button("Send")

    with col_send:
        st.write("")
        st.write("")
        if st.button("➡️", use_container_width=True, key="send_button_icon"):
            submitted = True

    if submitted:
        user_input = text_val.strip()
        st.session_state.pending_input = ""
    elif st.session_state.get("pending_input"):
        # Auto-send when speech recognized and no manual submit pressed
        user_input = st.session_state.pending_input.strip()
        st.session_state.pending_input = ""

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
