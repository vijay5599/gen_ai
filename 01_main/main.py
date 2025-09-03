from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()  # take environment variables from .env.


client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "hey I am Vijay.",
        }
    ],
)

print("Chat completion created", response.choices[0].message.content)


