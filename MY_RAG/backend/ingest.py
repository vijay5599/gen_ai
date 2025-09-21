import os
import openai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

openai.api_key = os.getenv(
    "OPENAI_API_KEY"
)
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

client = QdrantClient(url=QDRANT_URL)
COLLECTION_NAME = "financial_reports"


# Create collection if not exists
def init_collection():
    if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )


def embed_text(text: str):
    response = openai.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


def ingest_pdf(file_path: str, company: str, year: str):
    init_collection()
    reader = PdfReader(file_path)
    chunks = []
    for page in reader.pages:
        text = page.extract_text()
        if not text:
            continue
        # simple chunking
        for chunk in text.split("\n\n"):
            if len(chunk.strip()) > 50:
                chunks.append(chunk.strip())

    points = []
    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        points.append(
            PointStruct(
                id=i,
                vector=embedding,
                payload={"company": company, "year": year, "text": chunk},
            )
        )

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Ingested {len(points)} chunks from {file_path}")
