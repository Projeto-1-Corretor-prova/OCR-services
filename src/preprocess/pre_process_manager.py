from cv2 import (
    COLOR_BGR2GRAY,
    THRESH_BINARY,
    cvtColor,
    imread, 
    imwrite,
    threshold, 
)

from os import listdir
 
from src.preprocess.models import PreProcesserInput

from src.interfaces import PreProcessInterface

class PreProcessManager(PreProcessInterface):
    
    def __init__(self):
        super().__init__()
    
    def preprocess(self, pre_processer_input: PreProcesserInput) -> None:
        
        original_path = pre_processer_input['pre_process_path']
        
        students = [student for student in listdir(original_path)]
        
        paths_input = [f"{original_path}/{student}" for student in students]

        paths_output = [f"{pre_processer_input['pre_processed_dir_path']}/{student}" for student in students]
    
        for path_input, path_output in zip(paths_input, paths_output):
            for file in listdir(path_input):
                self.__preprocess_image(f"{path_input}/{file}", f"{path_output}/{file}")
    
    def __preprocess_image(self, path_input: str, path_output: str) -> None:
        image = imread(path_input)
        gray_image = cvtColor(image, COLOR_BGR2GRAY)
        _, binary_image = threshold(gray_image, 127, 255, THRESH_BINARY)
        
        imwrite(path_output, binary_image)