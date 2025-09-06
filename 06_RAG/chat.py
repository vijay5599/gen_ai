from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()  # take environment variables from .env.

openai_client = OpenAI()

# vector embedding
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    collection_name="pdf-collection",
    host="localhost",
    port=6333,
)

# take user query
query = input("Enter your query: ")

# returns relevant chunks from the vector db
search_results = vector_db.similarity_search(query=query)

context = "\n\n\n".join(
    [
        f"Page content: {doc.page_content} \n Page number: {doc.metadata['page_label']}"
        for doc in search_results
    ]
)
print(f"Context: {context}")
SYSTEM_PROMPT = """You are a helpful AI assistant. Use the following pieces of context to answer from the pdf file along with page_content and page number to the question at the end.
You should only answer the question based on the context provided.and navigate the user to open the right page number for more information.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Always answer in markdown format.
Context:
{context}
"""

# SYSTEM_PROMPT = """
# You are a helpful AI assistant.

# Use the provided context (which includes page_content and page_number from a PDF) to answer the user’s question.

# Guidelines:
# - Only use the information given in the context. Do not use outside knowledge.
# - Always reference the page_number where the answer can be found.
# - If the answer is not present in the context, respond with: "I don't know."
# - Provide the answer in clear and concise markdown format.
# - Help the user by guiding them to the correct page_number for more details.

# Context:
# {context}
# """

resposne = openai_client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query},
    ],
)

print(f"🤖 Answer: {resposne.choices[0].message.content}")
