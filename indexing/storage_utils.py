import boto3, uuid
from decouple import Config, RepositoryEnv
config = Config(repository=RepositoryEnv('.env'))

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
AWS_REGION_NAME = config("AWS_REGION_NAME", "us-east-1")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME,
)

def upload_file_to_s3(file_obj, filename_prefix="uploads"):
    """Uploads a file object to S3 and returns the file URL"""
    file_extension = file_obj.name.split(".")[-1]
    key = f"{filename_prefix}/{uuid.uuid4()}.{file_extension}"

    s3_client.upload_fileobj(file_obj, AWS_STORAGE_BUCKET_NAME, key)

    file_url = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION_NAME}.amazonaws.com/{key}"
    return file_url
