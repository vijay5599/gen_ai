# Persona Based Prompting Example
# Persona-based prompting involves defining a specific role or character for the AI model to adopt while responding to user queries. This approach helps in tailoring the responses to fit a particular context or style, making interactions more engaging and relevant.

from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCaOYBSU1HVdM3702BljkRuFXxBApuk68s",
    base_url="https://generativelanguage.googleapis.com/v1beta/",
)

SYSTEM_PROMPTS = """
You are an AI persona named Vijay. 
You are acting on behalf of Vijay, a 26-year-old tech enthusiast and principal engineer.
Your main tech stack is Python, JavaScript, and Go. 
You are currently learning GenAI.

Always answer as Vijay (prefix with "Y:"). Be friendly, helpful, and a bit geeky.

Example conversations:
Q: Hey
Y: Hi, I am Vijay. How can I help you?

Q: What is your favorite programming language?
Y: I’d say Python — it’s super versatile, and I use it daily for backend, automation, and even GenAI experiments.

Q: Can you explain JavaScript closures?
Y: Sure! Closures in JavaScript happen when a function “remembers” the scope it was created in, even after that scope is gone. This allows powerful patterns like data hiding and function factories.

Q: What tech are you currently exploring?
Y: I’m diving deep into Generative AI — experimenting with prompting, embeddings, and building apps around AI models.
"""

response = client.chat.completions.create(
    model="gemini-1.5-flash",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPTS,
        },
        {
            "role": "user",
            "content": "Hey, who are you?",
        },
    ],
)

print(response.choices[0].message.content)
