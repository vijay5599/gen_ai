# Zero Shot Prompting Example

from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCaOYBSU1HVdM3702BljkRuFXxBApuk68s",
    base_url="https://generativelanguage.googleapis.com/v1beta/",
)

# zero shot prompting: Directly asking the model to perform a task without any prior examples.
SYSTEM_PROMPTS = "You are a helpful assistant for coding related questions. Your name is Codiax, If the question is not related to coding, politely decline."

response = client.chat.completions.create(
    model="gemini-1.5-flash",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPTS,
        },
        {
            "role": "user",
            "content": "Hey, can you write a python function to reverse a string?",
        },
    ],
)

print(response.choices[0].message.content)
