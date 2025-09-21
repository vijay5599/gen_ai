import os
from openai import OpenAI
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()
# Initialize OpenAI client
client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Qdrant client
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "financial_reports"
client_qdrant = QdrantClient(url=QDRANT_URL)


def query_rag(question: str, company: str = None, year: str = None):
    # 🔹 Embed the question
    embedding = (
        client_openai.embeddings.create(model="text-embedding-3-small", input=question)
        .data[0]
        .embedding
    )

    # 🔹 Build filter if company/year provided
    query_filter = None
    if company or year:
        query_filter = {"must": []}
        if company:
            query_filter["must"].append({"key": "company", "match": {"value": company}})
        if year:
            query_filter["must"].append({"key": "year", "match": {"value": year}})

    # 🔹 Search Qdrant
    results = client_qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedding,
        limit=5,
        query_filter=query_filter,
    )

    context = "\n\n".join([r.payload["text"] for r in results])

    # 🔹 Send to GPT
    prompt = f"""
You are a financial assistant. Use the context below to answer the question.
If the answer is not in the context, say you don't know.

Context:
{context}

Question: {question}
Answer:
    """

    response = client_openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content.strip()
