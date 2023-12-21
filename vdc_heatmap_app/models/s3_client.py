from pydantic import BaseModel
from typing import Any, Dict
import boto3
from botocore.client import BaseClient


class S3Client(BaseModel):
    region_name: str
    access_key: str
    secret_key: str

    def get_client(self) -> BaseClient:
        """
        Returns an S3 client object.
        """
        return boto3.client(
            "s3",
            region_name=self.region_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        )

    def upload_file_to_bucket(
        self,
        file_path: str,
        file_name: str,
        bucket: str,
        content_type: str = "image/png",
    ) -> str:
        """
        Uploads a file to the specified S3 bucket.

        ## Parameters:
            file_path (str): The local file path of the file to be uploaded.
            file_name (str): The name of the file in the S3 bucket.
            bucket (str): The name of the S3 bucket.
            content_type (str, optional): The content type of the file. Defaults to "image/png".

        ## Returns:
            str: The ETag of the uploaded file.

        ## Raises:
            FileNotFoundError: If the specified file_path does not exist.
            botocore.exceptions.NoCredentialsError: If AWS credentials are not found.
            botocore.exceptions.ParamValidationError: If the provided parameters are invalid.
            botocore.exceptions.ClientError: If an error occurs during the S3 API call.
        """
        with open(file_path, "rb") as file:
            client = self.get_client()
            response: Dict[str, Any] = client.put_object(
                Body=file, Key=file_name, Bucket=bucket, ContentType=content_type
            )
            return response["ETag"]
