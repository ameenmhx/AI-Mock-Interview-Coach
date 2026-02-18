import ollama
from pypdf import PdfReader

# --- 1. READ AND CLEAN RESUME ---
print("Reading and cleaning resume...")
try:
    reader = PdfReader("resume.pdf")
    raw_text = ""
    for page in reader.pages:
        raw_text += page.extract_text() + "\n"
    
    # CLEANING: Remove extra spaces to speed up AI processing
    # Also limits text to first 1000 characters to save memory
    clean_text = raw_text.replace("  ", " ").strip()[:1000]
    print("Resume cleaned!\n")
except Exception as e:
    print(f"Error: {e}")
    exit()

job_description = "Junior Web Developer"

SYSTEM_PROMPT = f"""
You are an Interviewer for a {job_description} position.
Candidate Resume: {clean_text}

CRITICAL RULES:
1. Ask ONLY ONE short question at a time.
2. Use the candidate's name from the resume.
3. Ask about specific skills mentioned in the resume (like Python, HTML).
4. Be concise.
5. Start by greeting the candidate and asking them to introduce themselves.
"""

messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]

print("--- REAL RESUME INTERVIEW ---")
print("Interviewer: ", end="", flush=True)

response_stream = ollama.chat(
    model='phi3', 
    messages=messages, 
    stream=True,
    options={'temperature': 0.1}
)

full_response = ""
for chunk in response_stream:
    text = chunk['message']['content']
    print(text, end="", flush=True)
    full_response += text

messages.append({'role': 'assistant', 'content': full_response})
print()

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit': break

    messages.append({'role': 'user', 'content': user_input})
    
    print("Interviewer: ", end="", flush=True)
    response_stream = ollama.chat(
        model='phi3', 
        messages=messages, 
        stream=True,
        options={'temperature': 0.1}
    )
    
    full_response = ""
    for chunk in response_stream:
        text = chunk['message']['content']
        print(text, end="", flush=True)
        full_response += text
    
    messages.append({'role': 'assistant', 'content': full_response})
    print()