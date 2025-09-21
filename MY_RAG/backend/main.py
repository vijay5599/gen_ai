from fastapi import FastAPI, UploadFile, Form, File
from ingest import ingest_pdf
from rag import query_rag
import tempfile
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/ingest_pdf/")
async def ingest_endpoint(
    file: UploadFile = File(...), company: str = Form(...), year: str = Form(...)
):
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, file.filename)
    # file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    ingest_pdf(file_path, company, year)
    return {"status": "success", "file": file.filename}


@app.get("/query/")
async def query_endpoint(question: str, company: str = None, year: str = None):
    answer = query_rag(question, company, year)
    return {"question": question, "answer": answer}
