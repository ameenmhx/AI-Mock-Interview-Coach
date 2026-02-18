import ollama

# This is the "Brain" - The Instructions for the AI
SYSTEM_PROMPT = """
You are a strict Technical Hiring Manager.
Your task is to interview a candidate for a job.

RULES:
1. Ask only ONE question at a time.
2. Wait for the user to answer.
3. Be professional but concise.

Start by introducing yourself and asking the candidate to introduce themselves.
"""

# The conversation history (starts with the System Prompt)
messages = [
    {'role': 'system', 'content': SYSTEM_PROMPT}
]

print("--- Interview Coach Initialized ---")
print("The AI is starting the conversation...")
print("Type 'exit' to stop the program.\n")

# 1. Get the first message from the AI
response = ollama.chat(model='phi3', messages=messages)
ai_message = response['message']['content']

# 2. Show the AI's message
print(f"Interviewer: {ai_message}")

# 3. Add AI's message to history so it remembers
messages.append({'role': 'assistant', 'content': ai_message})

# 4. Start the Chat Loop
while True:
    user_input = input("You: ")
    
    if user_input.lower() == 'exit':
        break
    
    # Add user's answer to history
    messages.append({'role': 'user', 'content': user_input})
    
    # Ask AI for the next response
    response = ollama.chat(model='phi3', messages=messages)
    ai_reply = response['message']['content']
    
    print(f"Interviewer: {ai_reply}")
    
    # Add AI's reply to history
    messages.append({'role': 'assistant', 'content': ai_reply})