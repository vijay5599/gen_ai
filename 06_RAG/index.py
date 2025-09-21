from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

file_path = "./example_data/layout-parser-paper.pdf"


pdf_path = Path(__file__).parent / "python.pdf"

# load file in python pgm
loader = PyPDFLoader(file_path=pdf_path)
pages = loader.load()


# Cunking the documents into smaller pieces
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
''
chunks = text_splitter.split_documents(documents=pages)

# vector embedding
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
)

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    collection_name="pdf-collection",
    host="localhost",
    port=6333,
)

print(f"Total Chunks: {len(chunks)}")
