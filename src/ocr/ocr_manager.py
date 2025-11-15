from pytesseract import image_to_string

from PIL.Image import open as open_image

from src.interfaces import OCRInterface

from src.settings import Settings

from src.ocr.models import OCRResult

class OCRManager(OCRInterface):
    def __init__(self):
        super().__init__()

    def ocr(self, image_file_path: str) -> OCRResult:
        image_bytes = open_image(image_file_path)
        return {"ocr": image_to_string(image_bytes, lang=Settings.tesseract_language, config=Settings.tesseract_configuration)}