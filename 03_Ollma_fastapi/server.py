from fastapi import Body, FastAPI
from ollama import chat
from ollama import Client

app = FastAPI()

client = Client(
    host="http://localhost:11434",
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/chat")
def chat(message: str = Body(..., example="Hello, how are you?")):
    response = client.chat(
        model="gemma:2b",
        messages=[
            {
                "role": "user",
                "content": message,
            } 
        ],
    )
    return {"response": response.message.content}
