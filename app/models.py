from typing_extensions import TypedDict, Optional

from src.ocr.models import OCRResult

class ConsumeRequest(TypedDict):
    storage_path: str
    regex_question: str
    pre_process: Optional[bool] = True
    
class ProduceRequest(TypedDict):
    ocr_result: str