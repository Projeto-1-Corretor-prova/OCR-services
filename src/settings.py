from dotenv import load_dotenv

from os import getenv

load_dotenv()

class Settings:
    tesseract_language = getenv("TESSERACT_LANGUAGE")
    tesseract_configuration = getenv("TESSERACT_CONFIGURATION")
    consumer_threads = int(getenv("CONSUMER_THREADS"))
    
    redis_user = getenv("REDIS_USER")
    redis_password = getenv("REDIS_PASSWORD")
    redis_host = getenv("REDIS_URL")
    redis_port = getenv("REDIS_PORT")
    
    redis_encode = getenv("REDIS_ENCODE")
    redis_stream_consume_name = getenv("REDIS_STREAM_CONSUME_NAME")
    redis_stream_produce_name = getenv("REDIS_STREAM_PRODUCE_NAME")
    redis_consumer_group_name = getenv("REDIS_CONSUMER_GROUP_NAME") 
    redis_request_per_cycle = float(getenv("REDIS_REQUEST_PER_CYCLE"))
    redis_request_period_time = int(getenv("REDIS_REQUEST_PERIOD_TIME"))    
    
    storage_endpoint= getenv("STORAGE_ENDPOINT")
    storage_access_key= getenv("STORAGE_ACESS_KEY")
    storage_secret_access_key= getenv("STORAGE_SECRET_ACESS_KEY")
    storage_region= getenv("STORAGE_REGION")
    storage_bucket_name = getenv("STORAGE_BUCKET_NAME")
    