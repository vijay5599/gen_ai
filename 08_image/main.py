from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI


load_dotenv()
client = OpenAI()

respose = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Generate a caption for this image with 50 words.",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
                    },
                },
            ],
        }
    ],
)

print(respose.choices[0].message.content)
