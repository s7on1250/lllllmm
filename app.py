import streamlit as st
import backend

# Streamlit App
st.title("Law helper")

# Side panel for language selection
language = st.sidebar.selectbox("Choose language", ("English", "Russian"))

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Initialize session state for user input
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# Display chat history (messages)
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input with the value from session state
user_input = st.chat_input("Say something")

if user_input:
    # Add user message to chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Hide the input box and chat messages while waiting for bot response
    with st.spinner("Generating response..."):
        # Bot response based on selected language
        if language == "English":
            bot_response = "Hello!"  # Replace this with English bot logic
        else:
            # Call the backend for Russian response logic
            bot_response = backend.inference(st.session_state['messages'][-1]['content'])

        # Add bot response to chat history
        st.session_state["messages"].append({"role": "assistant", "content": bot_response})

    # Clear the input field after processing the message
    st.session_state["user_input"] = ""  # Reset input field value

    # Re-run the script to update the UI and show the response
    st.experimental_rerun()
