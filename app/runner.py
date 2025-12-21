from json import dumps

from app.files.file_manager import FileManager
from app.interfaces import BufferInterface

from src.consts import PROCESSED_FILES, ORIGINAL_FILES
from src.ocr.ocr_manager import OCRManager
from src.preprocess.pre_process_manager import PreProcessManager
from src.pipeline import Pipeline, PipelineModel

class Runner:
    
    __buffer_manager: BufferInterface
    __file_manager: FileManager
    __pipeline: Pipeline
    
    def __init__(self, bufer_manager: BufferInterface):
        self.__buffer_manager = bufer_manager
        self.__file_manager = FileManager()
        ocr_manager = OCRManager()
        pre_process_manager = PreProcessManager()
        self.__pipeline = Pipeline(pre_process_manager, ocr_manager)
    
    def run(self):
        """Run a consumer producer pattern in a Thread"""
        
        for metadata, consumer_request in self.__buffer_manager.consume():
            temp_folder = self.__file_manager.download(consumer_request["storage_path"])
        
            pipeline_input: PipelineModel = {
                "ocr_path": f"{temp_folder}/{PROCESSED_FILES}",
                "pre_process_path": f"{temp_folder}/{ORIGINAL_FILES}",
                "pre_processed_dir_path": f"{temp_folder}/{PROCESSED_FILES}",
                "regex_question": consumer_request["regex_question"],
                "pre_process": consumer_request["pre_process"]
            }
            
            ocr_result = self.__pipeline.run(pipeline_input)
            
            self.__buffer_manager.process(metadata)
            
            self.__buffer_manager.produce({"ocr_result": dumps(ocr_result)})
            
            self.__file_manager.remove(temp_folder)