from boto3 import resource

from os import makedirs
from os.path import relpath, join, dirname

from src.settings import Settings

class S3Manager:
    
    def __init__(self):
        self.__s3 = resource(
            "s3",
            endpoint_url=Settings.storage_endpoint,
            aws_access_key_id=Settings.storage_access_key,
            aws_secret_access_key=Settings.storage_secret_access_key,
            region_name=Settings.storage_region,
        )
        
        print("Bucket:", Settings.bucket_name)
        print("Cliente:", self.__s3)
        
    
    def download(self, storage_path: str, local_path: str) -> None:
        """Download written tests from minio

        Args:
            storage_path (str): storage_path
            local_path (str): local path (to download)
        """
        
        bucket = self.__s3.Bucket(Settings.bucket_name)

        # garante barra final
        if not storage_path.endswith("/"):
            storage_path += "/"

        for obj in bucket.objects.filter(Prefix=storage_path):
            if obj.key.endswith("/"):
                continue

            relative_path = relpath(obj.key, storage_path)
            local_file_path = join(local_path, relative_path)

            makedirs(dirname(local_file_path), exist_ok=True)

            bucket.download_file(obj.key, local_file_path)