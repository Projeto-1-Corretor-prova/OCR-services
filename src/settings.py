from dotenv import load_dotenv

from os import getenv

load_dotenv()

class Settings:
    tesseract_language = getenv("TESSERACT_LANGUAGE")
    tesseract_configuration = getenv("TESSERACT_CONFIGURATION")
    storage_endpoint= getenv("STORAGE_ENDPOINT")
    storage_access_key= getenv("STORAGE_ACESS_KEY")
    storage_secret_access_key= getenv("STORAGE_SECRET_ACESS_KEY")
    storage_region= getenv("STORAGE_REGION")
    bucket_name = getenv("STORAGE_BUCKET_NAME")