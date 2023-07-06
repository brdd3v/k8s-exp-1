import socket
from fastapi import FastAPI
from redis import Redis


app = FastAPI()
redis = Redis(host='redis', port=6379)


@app.get("/")
def read_root():
    hostname = socket.gethostname()
    count = redis.incr(f"container_{hostname}")
    return f"This webpage has been viewed {count} time(s) [{hostname}]"
