import streamlit as st
import backend

# Streamlit App
st.title("Law Helper")

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Files")
    uploaded_files = st.file_uploader("Upload your files here", accept_multiple_files=True)

    if uploaded_files:
        st.write(f"Uploaded {len(uploaded_files)} file(s):")
        for file in uploaded_files:
            st.write(f"- {file.name}")
            # Optionally process each file using the backend
            # Example: backend.process_file(file)

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Layout with columns for main chat and additional input on the right
col1, col_ex = st.columns([3, 1])  # Adjust column width ratio if necessary
with col_ex:
    st.subheader("Example Q/A")
    extra_input = st.text_area("Enter additional info:", height=200)
# Column 1: Main chat interface
with col1:
    # Process user input or example prompt
    user_input = st.chat_input("Say something") or st.session_state.get("user_input")

    if user_input:
        # Add user message to chat history
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Hide the input box and chat messages while waiting for bot response
        with st.spinner("Generating response..."):
            # Bot response based on selected language
            bot_response = backend.inference(user_input, uploaded_files, extra_input)

            # Add bot response to chat history
            st.session_state["messages"].append({"role": "assistant", "content": bot_response})

        # Clear the input field and reset user input state
        st.session_state["user_input"] = None  # Reset after processing
        st.rerun()  # Re-run to update the chat UI

    # Display chat history (messages)
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
