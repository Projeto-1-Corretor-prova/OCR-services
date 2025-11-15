from dotenv import load_dotenv

from os import getenv

load_dotenv()

class Settings:
    tesseract_language = getenv("TESSERACT_LANGUAGE")
    tesseract_configuration = getenv("TESSERACT_CONFIGURATION")