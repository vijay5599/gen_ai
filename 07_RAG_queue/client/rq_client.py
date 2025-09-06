from redis import Redis
from rq import Queue, Worker

listen = ["default"]

# Redis connection
conn = Redis(host="localhost", port=6379)

# main queue
queue = Queue(connection=conn)

if __name__ == "__main__":
    queues = [Queue(name, connection=conn) for name in listen]
    worker = Worker(queues, connection=conn)
    # run worker in non-forking mode (Windows safe)
    worker.work(with_scheduler=True)

Kiran@1234567