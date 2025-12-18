from os import mkdir, listdir
from os.path import exists

from re import match

from src.interfaces import OCRInterface, PreProcessInterface
from src.ocr.models import OCRInput, OCRResult
from src.preprocess.models import PreProcesserInput

class PipelineModel(PreProcesserInput, OCRInput):
    pass
    
class Pipeline:

    __pre_processer: PreProcessInterface
    __ocr_manager: OCRInterface

    def __init__(self, pre_processer: PreProcessInterface, ocr_manager: OCRInterface):
        self.__pre_processer = pre_processer
        self.__ocr_manager = ocr_manager
        
    def run(self, pipeline_input: PipelineModel) -> OCRResult:
        """ OCR pipeline execution, after pre process the pictures, generate the OCR

        Args:
            pre_processer_input (PipelineModel): Pipeline input

        Returns:
            OCRResult: Ocr Result
        """
        
        original_path = pipeline_input["pre_process_path"]
        
        if not exists(original_path):
            raise NotADirectoryError("Original path not found.")
        
        students = [f"{original_path}/{student}" for student in listdir(original_path)]
        
        if not any(students):
            raise FileNotFoundError("No student found.")
        
        self.__pre_processer.preprocess({
            "pre_process_path": pipeline_input["pre_process_path"],
            "pre_processed_dir_path": pipeline_input["pre_processed_dir_path"]
            })
        
        ocr_result = self.__ocr_manager.ocr({
            "ocr_path": pipeline_input["pre_processed_dir_path"],
            "regex_question": pipeline_input["regex_question"]
        })
        
        return ocr_result        