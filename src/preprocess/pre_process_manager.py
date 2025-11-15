from cv2 import (
    cvtColor, 
    imread, 
    imwrite, 
    threshold, 
    imshow
)
 
from cv2 import COLOR_BGR2GRAY, THRESH_BINARY

from src.interfaces import PreProcessInterface

class PreProcessManager(PreProcessInterface):
    
    def __init__(self):
        super().__init__()
    
    def preprocess(self, image_file_path: str, output_path: str) -> None:
        image = imread(image_file_path)
        gray_image = cvtColor(image, COLOR_BGR2GRAY)
        _, binary_image = threshold(gray_image, 127, 255, THRESH_BINARY)
        
        imwrite(output_path, binary_image)