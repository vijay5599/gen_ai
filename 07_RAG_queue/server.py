from fastapi import FastAPI, Query
from .queue.workder import process_query
from .client.rq_client import queue
from fastapi import FastAPI, Query
from redis import Redis
from rq import Queue

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/chat")
def chat(query: str = Query(..., description="The user query")):
    job = queue.enqueue(process_query, query)
    return {"job_id": job.id, "status": "queued"}


@app.get("/result")
def get_result(job_id: str = Query(..., description="The job ID")):
    job = queue.fetch_job(job_id)
    res = job.return_value()
    return {"job_id": job_id, "result": res}
