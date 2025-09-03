from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCaOYBSU1HVdM3702BljkRuFXxBApuk68s",
    base_url="https://generativelanguage.googleapis.com/v1beta/",
)


response = client.chat.completions.create(
    model="gemini-1.5-flash",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant for Math problems. If the question is not related to Math, politely decline.",
        },
        {
            "role": "user",
            "content": "Hey, can you help me with a math problem? What is 2+2?",
        },
    ],
)

print(response.choices[0].message.content)
