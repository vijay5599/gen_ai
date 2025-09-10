import json
import os
from mem0 import Memory
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

config = {
    "vesion": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {"api_key": OPENAI_API_KEY, "model": "text-embedding-3-small"},
    },
    "llm": {
        "provider": "openai",
        "config": {"api_key": OPENAI_API_KEY, "model": "gpt-4.1-mini"},
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
        },
    },
}

mem_client = Memory.from_config(config)

while True:
    user_query = input("Enter your query:> ")
    search_memory = mem_client.search(user_id="Vijay", query=user_query)
    memories = [
        f"ID: {item.get("id")}\nMemory:{item.get("memory")}"
        for item in search_memory.get("results", [])
    ]

    SYSTEM_PROMPT = f"""Here is the relevant context from the memory:
    {json.dumps(memories)}"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
        ],
    )
    print("Response:", response.choices[0].message.content)

    mem_client.add(
        user_id="Vijay",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": response.choices[0].message.content},
        ],
    )

    print("Memory stored successfully.")
