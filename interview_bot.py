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
# We will hardcode a target job for this test
job_description = """
Role: Junior Web Developer
Requirements:
- Good knowledge of HTML, CSS, and JavaScript.
- Basic Python skills.
- Understanding of Databases.
"""

# --- PART 3: CREATE THE INTERVIEWER BRAIN ---
SYSTEM_PROMPT = f"""
You are a strict Technical Hiring Manager.
You are interviewing a candidate for this Job:
{job_description}

The candidate has uploaded this Resume:
{resume_text}

INSTRUCTIONS:
1. Analyze the resume against the job description.
2. Start by welcoming the candidate (use their name from the resume).
3. Ask specific questions based on the skills mentioned in the resume.
4. If the resume mentions a project, ask details about it.
5. Ask ONE question at a time.
"""

# --- PART 4: THE CHAT LOOP ---
messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]

print("--- INTERVIEW STARTED (Type 'exit' to quit) ---")

# AI says hello first
response = ollama.chat(model='phi3', messages=messages)
ai_msg = response['message']['content']
print(f"Interviewer: {ai_msg}")
messages.append({'role': 'assistant', 'content': ai_msg})

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit': break

    messages.append({'role': 'user', 'content': user_input})
    
    response = ollama.chat(model='phi3', messages=messages)
    ai_reply = response['message']['content']
    
    print(f"Interviewer: {ai_reply}")
    messages.append({'role': 'assistant', 'content': ai_reply})