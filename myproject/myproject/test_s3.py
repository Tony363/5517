import boto3
import os
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
import os


def upload_to_s3(file_name, bucket, object_name=None):
    """
    Upload a file to an S3 bucket using credentials from environment variables

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified, file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name
    # Load the environment variables from .env file
    load_dotenv('aws_secrets.env')
    # Get credentials from environment variables
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    # Create an S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    try:
        # Upload the file
        s3_client.upload_file(file_name, bucket, object_name)
    except NoCredentialsError:
        print("Credentials not available")
        return False
    return True

if __name__ == "__main__":
    # Example usage:
    uploaded = upload_to_s3('/home/tony/Desktop/5517/myproject/documents/5511_hw3_early_stop.pdf', 'documents-5517', '5511-hw3.pdf')
    if uploaded:
        print("File uploaded successfully.")
    else:
        print("Upload failed.")
