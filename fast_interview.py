import ollama
from pypdf import PdfReader

# --- PART 1: READ THE RESUME ---
print("Reading resume.pdf...")
try:
    reader = PdfReader("resume.pdf")
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text() + "\n"
    print("Resume loaded successfully!\n")
except Exception as e:
    print(f"Error reading PDF: {e}")
    exit()

# --- PART 2: SET THE JOB DESCRIPTION ---
job_description = "Junior Web Developer role requiring HTML, CSS, and Python."

# --- PART 3: CREATE THE INTERVIEWER BRAIN ---
# We keep the prompt simple to ensure speed
SYSTEM_PROMPT = f"""
You are a Hiring Manager.
Interview the candidate for a {job_description} role.
Their Resume: {resume_text}
Ask short questions one by one. Start now.
"""

messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]

print("--- INTERVIEW STARTED (Type 'exit' to quit) ---")
print("Interviewer: ", end="", flush=True)

# STREAMING MODE: Prints word by word
response_stream = ollama.chat(model='phi3', messages=messages, stream=True)

full_response = ""
for chunk in response_stream:
    text = chunk['message']['content']
    print(text, end="", flush=True)
    full_response += text

print() # New line
messages.append({'role': 'assistant', 'content': full_response})

# --- PART 4: THE CHAT LOOP ---
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit': break

    messages.append({'role': 'user', 'content': user_input})
    
    print("Interviewer: ", end="", flush=True)
    response_stream = ollama.chat(model='phi3', messages=messages, stream=True)
    
    full_response = ""
    for chunk in response_stream:
        text = chunk['message']['content']
        print(text, end="", flush=True)
        full_response += text
    
    print() # New line
    messages.append({'role': 'assistant', 'content': full_response})