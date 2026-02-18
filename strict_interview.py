import ollama

resume_text = "My name is Ameen. I know Python and HTML."
job_description = "Junior Web Developer"

# STRICT PROMPT
SYSTEM_PROMPT = f"""
You are an Interviewer for a {job_description} position.
Resume: {resume_text}

RULES:
1. Ask ONLY ONE question at a time.
2. Do NOT use bullet points or lists.
3. Keep your sentences short.
4. Wait for the user to answer.
5. Start by asking for the candidate's name.
"""

messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]

print("--- INTERVIEW STARTED (Strict Mode) ---")
print("Interviewer: ", end="", flush=True)

# Stream response
response_stream = ollama.chat(model='phi3', messages=messages, stream=True)
full_response = ""
for chunk in response_stream:
    text = chunk['message']['content']
    print(text, end="", flush=True)
    full_response += text

messages.append({'role': 'assistant', 'content': full_response})
print()

# Chat Loop
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
    
    messages.append({'role': 'assistant', 'content': full_response})
    print()