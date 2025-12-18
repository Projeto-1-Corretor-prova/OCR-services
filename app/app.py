from fastapi import FastAPI

from app.files.file_manager import FileManager

from src.consts import ORIGINAL_FILES, PROCESSED_FILES
from src.ocr import OCRManager
from src.pipeline import Pipeline, PipelineModel, OCRResult
from src.preprocess import PreProcessManager

from pathlib import Path

from shutil import copyfileobj

from uuid import uuid4

TEMP_DIR = "temp"

app = FastAPI()

ocr_manager = OCRManager()
pre_process_manager = PreProcessManager()

pipeline = Pipeline(pre_process_manager, ocr_manager)

file_manager = FileManager()

from typing_extensions import TypedDict

class Input(TypedDict):
    storage_path: str
    regex_question: str

@app.post("/extract-answers")
def extract_text_from_image(input_api: Input) -> OCRResult:
    
    storage_path = input_api["storage_path"]
    
    temp_folder = file_manager.download(storage_path)
    
    pipeline_input: PipelineModel = {
        "ocr_path": f"{temp_folder}/{PROCESSED_FILES}",
        "pre_process_path": f"{temp_folder}/{ORIGINAL_FILES}",
        "pre_processed_dir_path": f"{temp_folder}/{PROCESSED_FILES}",
        "regex_question": input_api["regex_question"]
    }
    
    ocr_result = pipeline.run(pipeline_input)
    
    return ocr_result