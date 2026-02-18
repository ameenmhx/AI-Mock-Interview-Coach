import ollama

resume_text = "My name is Ameen. I know Python and HTML."
job_description = "Junior Web Developer"

# VERY STRICT PROMPT
SYSTEM_PROMPT = f"""
You are an Interviewer for a {job_description} position.
Resume: {resume_text}

CRITICAL RULES:
1. You MUST ask ONLY ONE short question at a time.
2. NEVER ask multiple questions.
3. NEVER use bullet points.
4. Be concise.
5. Start by asking: 'Hello, what is your name?'
"""

messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]

print("--- FAST INTERVIEW MODE ---")
print("Interviewer: ", end="", flush=True)

# Added 'options' to lower temperature (make it smarter/stricter)
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