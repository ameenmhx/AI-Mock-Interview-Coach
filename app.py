import streamlit as st
from groq import Groq
from pypdf import PdfReader
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Career Coach", layout="wide")
st.title("🤖 AI Career Coach")

# --- INIT GROQ CLIENT ---
# Automatically uses the key from .streamlit/secrets.toml
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- SIDEBAR: SETUP ---
with st.sidebar:
    st.header("Setup")
    
    # Mode Selector
    mode = st.radio("Choose Mode:", ["Interview Simulation", "Write My CV"])
    
    uploaded_file = st.file_uploader("Upload Existing Resume (Optional)", type="pdf")
    job_desc = st.text_area("Paste Target Job Description", height=150)
    
    # For CV Writer
    if mode == "Write My CV":
        user_details = st.text_area("Your Raw Details (Education, Skills, Projects)", height=150)

    if st.button("Start"):
        st.session_state.interview_started = True
        
        # Read PDF
        resume_text = ""
        if uploaded_file:
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                resume_text += page.extract_text()
            resume_text = resume_text.replace("  ", " ").strip()
        else:
            resume_text = "No resume uploaded."

        # Dynamic Prompt
        if mode == "Interview Simulation":
            system_prompt = f"""
            You are a Hiring Manager for this job: {job_desc}.
            Candidate Resume: {resume_text}
            RULES: Ask ONE short question at a time. Start now.
            """
        else: # Write CV Mode
            raw_info = st.session_state.get('user_details_input', '')
            system_prompt = f"""
            You are an expert Resume Writer.
            Target Job: {job_desc}
            Candidate Info: {raw_info}
            Existing Resume Text: {resume_text}
            
            TASK: Write a professional, clean resume structure suitable for this job. 
            Use bullet points for skills. Keep it concise.
            """

        st.session_state.messages = [{'role': 'system', 'content': system_prompt}]
        st.session_state.chat_history = []
        st.rerun()

# --- MAIN CHAT AREA ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

# Display Chat History
for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.write(message['content'])

# Chat Input
if prompt := st.chat_input("Type here..."):
    st.session_state.chat_history.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.write(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    with st.chat_message('assistant'):
        # GROQ API CALL (Streaming)
        response_stream = client.chat.completions.create(
            model="llama-3.1-8b-instant", # UPDATED MODEL NAME
            messages=st.session_state.messages,
            stream=True
        )
        
        # Handle the Groq stream format
        def stream_generator():
            for chunk in response_stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

        response_text = st.write_stream(stream_generator)
        
        st.session_state.messages.append({'role': 'assistant', 'content': response_text})
        st.session_state.chat_history.append({'role': 'assistant', 'content': response_text})

# Initial Greeting
if st.session_state.interview_started and len(st.session_state.chat_history) == 0:
    with st.chat_message('assistant'):
        with st.spinner("Thinking..."):
            response_stream = client.chat.completions.create(
                model="llama-3.1-8b-instant", # UPDATED MODEL NAME
                messages=st.session_state.messages,
                stream=True
            )
            
            def stream_generator():
                for chunk in response_stream:
                    if chunk.choices[0].delta.content is not None:
                        yield chunk.choices[0].delta.content
            
            response_text = st.write_stream(stream_generator)
            
            st.session_state.messages.append({'role': 'assistant', 'content': response_text})
            st.session_state.chat_history.append({'role': 'assistant', 'content': response_text})
            st.rerun()
            
# Capture raw details for CV mode
if mode == "Write My CV":
    st.session_state['user_details_input'] = user_details