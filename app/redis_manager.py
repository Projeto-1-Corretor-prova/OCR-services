from redis import Redis

from logging import getLogger, Logger
from time import sleep
from threading import get_native_id
from uuid import uuid4

from app.interfaces import BufferInterface
from app.models import ConsumeRequest

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
            self.__logger.warning(f"Redis creation group - consume - error: {e}")

        try:
            self.__redis.xgroup_create(Settings.redis_stream_produce_name, Settings.redis_consumer_group_name, "$", mkstream=True)
        except Exception as e:
            self.__logger.warning(f"Redis creation group - produce - error: {e}")

    def consume(self):
        while True:
            response = self.__redis.xreadgroup(
                streams={Settings.redis_stream_consume_name: ">"},
                consumername=f"Consumer {self.__random_tag}",
                groupname=Settings.redis_consumer_group_name,
                count=Settings.redis_request_period_time,
            )
            
            if not response:
                sleep(Settings.redis_request_period_time)
                continue
            
            stream_response = response[0]
            
            stream_result = stream_response[1]
            
            if not any(stream_result):
                sleep(Settings.redis_request_period_time)
                continue
            
            self.__logger.debug("Response consumed")
            
            for metadata, consume_request in stream_result:
                self.__logger.debug(f"Response id: {metadata}, consumed!")
                yield metadata, self.__fix_encode(consume_request)
                
    def process(self, metadata):
        try:
            self.__redis.xack(Settings.redis_stream_consume_name, Settings.redis_consumer_group_name, metadata)
            self.__logger.debug(f"Response id: {metadata}, processed successful.")
        except Exception as ex:
            self.__logger.error(f"Redis Error Acknowledgement, error: {ex}")
    
    def produce(self, produce_request):
        try:
            id = self.__redis.xadd(Settings.redis_stream_produce_name, produce_request)
            self.__logger.debug(f"Response id: {id}, produced successful - Producer channel.")
        except Exception as e:
            self.__logger.error(f"Redis Error On Add Stream on Produce, error: {e}")
    
    def add(self, consume_request):
        try:
            id = self.__redis.xadd(Settings.redis_stream_consume_name, consume_request)
            self.__logger.debug(f"Response id: {id}, produced successful - Consumer channel.")
        except Exception as e:
            self.__logger.error(f"Redis Error On Add Stream on Consume, error: {e}")
    
    def __fix_encode(self, stream_response: dict[bytes, bytes]) -> ConsumeRequest:
        """ Fix encoding on stream response.

        Args:
            stream_response (dict[bytes, bytes]): Stream response from redis manager (consumer channel)

        Returns:
            ConsumeRequest: Consumer request
        """
        
        consume_request: ConsumeRequest = dict()
        
        for key in stream_response:
            consume_request[key.decode(Settings.redis_encode)] = stream_response[key].decode(Settings.redis_encode) 
            
        consume_request["pre_process"] = bool(consume_request["pre_process"])
        
        return consume_request