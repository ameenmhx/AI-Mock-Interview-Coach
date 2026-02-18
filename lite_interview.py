import ollama

# We are NOT reading the PDF right now to save memory.
# We will just use this small text as a fake resume.
resume_text = "My name is Ameen. I know Python and HTML."

job_description = "Junior Web Developer"

SYSTEM_PROMPT = f"""
You are a Hiring Manager for a {job_description} position.
The candidate's resume is: {resume_text}
Ask short questions. Start by asking their name.
"""

messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]

print("--- LITE MODE STARTED ---")
print("Interviewer: ", end="", flush=True)

# Stream the response
try:
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

except Exception as e:
    print(f"\nError: {e}")