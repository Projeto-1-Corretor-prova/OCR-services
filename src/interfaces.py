from abc import ABC

class PreProcessInterface(ABC):
    def preprocess(self, image_file_path: str, output_path: str) -> None:
        """Pre process a image from original path.

        Args:
            image_file_path (str): original image path.
            output_path (str): original image pre processed final path.
        """
        raise NotImplementedError("This is just a interface method!")
    
class OCRInterface(ABC):
    def ocr(self, image_file_path: str) -> str:
        """Optical Character Recognition from image file path.

        Args:
            image_file_path (str): Original image path.

        Returns:
            str: Optical characters recognized.
        """
        raise NotImplementedError("This is just a interface method!")