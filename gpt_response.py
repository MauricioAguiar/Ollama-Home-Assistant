from ollama import chat


stream = chat(
    model='GlaDos',
    messages=[{'role': 'user', 'content': 'Can you turn the light off?'}],
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)