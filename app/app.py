from fastapi import FastAPI

from threading import Thread

from app.models import ConsumeRequest
from app.queue_manager import Runner
from app.redis_manager import RedisManager

from src.settings import Settings

app = FastAPI()

redis_manager = RedisManager()

def run_consume():
    redis_manager = RedisManager()
    queue_manager = Runner(redis_manager)
    queue_manager.run()

threads = [Thread(target=run_consume, args=()) for _ in range(Settings.consumer_threads)]

for t in threads:
    t.start()

@app.post("/consume-request")
def extract_text_from_image(consume_request: ConsumeRequest) -> None:
    redis_manager.add(consume_request)
