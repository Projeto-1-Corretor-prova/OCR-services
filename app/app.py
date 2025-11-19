from fastapi import FastAPI, UploadFile

from src.ocr import OCRManager, OCRResult
from src.preprocess import PreProcessManager

from os import mkdir, remove
from os.path import exists

from pathlib import Path

from shutil import copyfileobj

from uuid import uuid4

TEMP_DIR = "temp"

app = FastAPI()

ocr_manager = OCRManager()
pre_process_manager = PreProcessManager()

if not exists(TEMP_DIR):
    mkdir(TEMP_DIR)

@app.post("/extract-text-from-image")
def extract_text_from_image(image: UploadFile) -> OCRResult:
    id_image = uuid4()
    
    file_name_path = Path(image.filename)
    
    with open(f"{TEMP_DIR}/{id_image}{file_name_path.suffix}", 'wb') as f:
        copyfileobj(image.file, f)
        
    pre_process_manager.preprocess(f"{TEMP_DIR}/{id_image}{file_name_path.suffix}", f"{TEMP_DIR}/{id_image}-preprocessed{file_name_path.suffix}")
    
    ocr = ocr_manager.ocr(f"{TEMP_DIR}/{id_image}-preprocessed{file_name_path.suffix}")
    
    remove(f"{TEMP_DIR}/{id_image}{file_name_path.suffix}")
    remove(f"{TEMP_DIR}/{id_image}-preprocessed{file_name_path.suffix}")
    
    return ocr