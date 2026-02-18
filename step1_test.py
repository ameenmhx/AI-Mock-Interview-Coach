import ollama

# We are sending a simple test message to Phi-3
response = ollama.chat(model='phi3', messages=[
    {
        'role': 'user',
        'content': 'Hello! Say "I am ready to interview you" in a professional tone.',
    },
])

print(response['message']['content'])