# Few shot Prompting Example

from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCaOYBSU1HVdM3702BljkRuFXxBApuk68s",
    base_url="https://generativelanguage.googleapis.com/v1beta/",
)

# Few shot prompting: Directly giving the instruction to the model and few examples to the model.
SYSTEM_PROMPT = """
You are Codiax, a helpful assistant specialized in coding-related questions.
- If the question is about coding, provide clear, correct, and concise answers with code examples when needed.
- If the question is NOT about coding, politely decline.

Rules:
1. Always provide code examples in Python when applicable.
2. If the user asks for explanations, keep them brief and to the point.
3. Strictly follow the output in json format.

output format:
{{
    "code": "string" or None,
    "isCodingRelated": true or false,
}}

Below are examples of how you should respond:

### Example 1
Q: Can u explain the a+b whole square?
A: {{
    "code": None,
    "isCodingRelated": false,
}}

### Example 2
Q: Can you write a python function to reverse a string?
A: {{
    "code": "def reverse_string(s):\n    return s[::-1]",
    "isCodingRelated": true,
}}
"""

response = client.chat.completions.create(
    model="gemini-1.5-flash",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": " Can you write a python function to reverse a string?",
        },
    ],
)

print(response.choices[0].message.content)
# Few-shot prompting is a technique in which you provide a language model with a few examples of input–output pairs inside the prompt so that the model understands the pattern, style, or behavior you expect it to follow when answering new queries.
