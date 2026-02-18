import streamlit as st
import ollama
from pypdf import PdfReader

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Mock Interview Coach", layout="wide")
st.title("🤖 AI Mock Interview Coach")

# --- SIDEBAR: SETUP ---
with st.sidebar:
    st.header("Setup Interview")
    uploaded_file = st.file_uploader("1. Upload Resume (PDF)", type="pdf")
    job_desc = st.text_area("2. Paste Job Description", "Junior Web Developer")
    
    # Button to start
    if st.button("Start Interview"):
        st.session_state.interview_started = True
        
        # Read PDF if uploaded
        resume_text = ""
        if uploaded_file:
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                resume_text += page.extract_text()
            # Clean text
            resume_text = resume_text.replace("  ", " ").strip()
        else:
            resume_text = "No resume uploaded."

        # Set the System Prompt
        st.session_state.messages = [{
            'role': 'system',
            'content': f"""
            You are a Hiring Manager for a {job_desc} position.
            Resume: {resume_text}
            RULES:
            1. Ask ONE short question at a time.
            2. Use the candidate's name.
            3. Start now.
            """
        }]
        st.session_state.chat_history = [] # Clear visual history
        st.rerun() # Refresh the app

# --- MAIN CHAT AREA ---

# Initialize session state variables if they don't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

# Display Chat History (The visual bubbles)
for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.write(message['content'])

# The Chat Input Box
if prompt := st.chat_input("Type your answer here..."):
    # 1. Add user message to history
    st.session_state.chat_history.append({'role': 'user', 'content': prompt})
    
    # Display user message immediately
    with st.chat_message('user'):
        st.write(prompt)

    # 2. Add to AI memory
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    # 3. Get AI response
    with st.chat_message('assistant'):
        # Stream the response
        response_stream = ollama.chat(
            model='phi3', 
            messages=st.session_state.messages, 
            stream=True,
            options={'temperature': 0.1}
        )
        
        # Write word by word
        response_text = st.write_stream(chunk['message']['content'] for chunk in response_stream)
        
        # Save to AI memory
        st.session_state.messages.append({'role': 'assistant', 'content': response_text})
        # Save to visual history
        st.session_state.chat_history.append({'role': 'assistant', 'content': response_text})

# Initial Greeting Logic
if st.session_state.interview_started and len(st.session_state.chat_history) == 0:
    with st.chat_message('assistant'):
        with st.spinner("Thinking..."):
            response_stream = ollama.chat(
                model='phi3', 
                messages=st.session_state.messages, 
                stream=True,
                options={'temperature': 0.1}
            )
            response_text = st.write_stream(chunk['message']['content'] for chunk in response_stream)
            
            st.session_state.messages.append({'role': 'assistant', 'content': response_text})
            st.session_state.chat_history.append({'role': 'assistant', 'content': response_text})
            st.rerun()