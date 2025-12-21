from fastapi import FastAPI

from logging import basicConfig, getLogger
from threading import Thread

from app.models import ConsumeRequest
from app.runner import Runner
from app.redis_manager import RedisManager

from src.settings import Settings

basicConfig(level=Settings.log_level)

logger = getLogger(__name__)

app = FastAPI()

logger.debug("fastApi initialized!")

redis_manager = RedisManager()

logger.debug("Redis manager to add on consumer chanell initialized!")

def run_consume():
    redis_manager = RedisManager()
    queue_manager = Runner(redis_manager)
    queue_manager.run()

threads = [Thread(target=run_consume, args=()) for _ in range(Settings.consumer_threads)]

logger.debug("Consumers Threads created!")

for t in threads:
    t.start()

logger.debug("Consumer Threads started executions")

@app.post("/consume-request")
def extract_text_from_image(consume_request: ConsumeRequest) -> None:
    consume_request["pre_process"] = int(consume_request["pre_process"])
    redis_manager.add(consume_request)
