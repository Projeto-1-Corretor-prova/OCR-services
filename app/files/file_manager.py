from os import mkdir, listdir

from os.path import exists

from shutil import rmtree

from uuid import uuid4

from src.consts import ORIGINAL_FILES, PROCESSED_FILES

from app.files.s3_manager import S3Manager

TEMP_FILE = "temp"

class FileManager:
    
    __s3_manager: S3Manager
    
    def __init__(self):
        if not exists(TEMP_FILE):
            mkdir(TEMP_FILE)
    
        self.__s3_manager = S3Manager()

    def download(self, storage_written_test_path: str) -> str:
        """download answered written tests from storage

        Args:
            storage_written_test_path (str): storage written test path

        Returns:
            str: temp path on file system
        """
        
        temp_folder_name = f"{TEMP_FILE}/{uuid4()}"
        
        while exists(temp_folder_name):
            temp_folder_name = f"{TEMP_FILE}/{uuid4()}"
            
        mkdir(temp_folder_name)
        
        temp_folder_name_original = f"{temp_folder_name}/{ORIGINAL_FILES}"
        
        temp_folder_name_processed = f"{temp_folder_name}/{PROCESSED_FILES}"
        
        mkdir(temp_folder_name_original)
        
        mkdir(temp_folder_name_processed)
        
        self.__s3_manager.download(storage_written_test_path, temp_folder_name_original)
        
        for student in listdir(temp_folder_name_original):
            mkdir(f"{temp_folder_name_processed}/{student}")
            
        return temp_folder_name
    
    def remove(self, temp_dir: str) -> None:
        """ Remove temp dir

        Args:
            temp_dir (str): temp dir
        """
        rmtree(temp_dir)