from redis import Redis

from logging import getLogger, Logger
from time import sleep
from threading import get_native_id
from uuid import uuid4

from app.interfaces import BufferInterface
from src.settings import Settings

class RedisManager(BufferInterface):

    __redis: Redis
    __logger: Logger
    __random_tag: str
    
    def __init__(self):
        self.__logger = getLogger(__name__)
        self.__random_tag = uuid4()
        self.__logger.debug(f"Random tag: {self.__random_tag} for the thread number: {get_native_id()}")
        self.__redis = Redis(
            host=Settings.redis_host,
            port=Settings.redis_port,
            username=Settings.redis_user,
            password=Settings.redis_password
        )
        
        try:
            self.__redis.xgroup_create(Settings.redis_stream_consume_name, Settings.redis_consumer_group_name, "$", mkstream=True)
        except Exception as e:
            self.__logger.warning(f"Redis error: {e}")

    def consume(self):
        while True:
            response = self.__redis.xreadgroup(
                streams={Settings.redis_stream_consume_name: 0},
                consumername=f"Consumer {self.__random_tag}",
                groupname=Settings.redis_consumer_group_name,
                count=Settings.redis_request_period_time,
            )
            
            _, stream_result = response[0][0]
            
            print(f" {stream_result}")
    
            if not any(stream_result):
                sleep(Settings.redis_request_period_time)
                
            self.__logger.debug("Responses claimed")
            
            for metadata, consume_request in response:
                yield metadata, consume_request
                
    def process(self, metadata):
        try:
            self.__redis.xack(Settings.redis_stream_consume_name, Settings.redis_consumer_group_name, metadata)
        except Exception as ex:
            self.__logger.error(f"Redis Error Acknowledgement, error: {ex}")
    
    def produce(self, produce_request):
        try:
            self.__redis.xadd(Settings.redis_stream_produce_name, produce_request)
        except Exception as e:
            self.__logger.error(f"Redis Error On Add Stream on Produce, error: {e}")
    
    def add(self, consume_request):
        try:
            self.__redis.xadd(Settings.redis_stream_consume_name, consume_request)
        except Exception as e:
            self.__logger.error(f"Redis Error On Add Stream on Consume, error: {e}")
    