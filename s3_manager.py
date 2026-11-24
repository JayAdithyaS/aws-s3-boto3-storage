import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = "jay-cloud-storage-boto3"
LOCAL_FILE = "sample.txt"
S3_KEY = "uploads/sample.txt"
DOWNLOAD_PATH = "downloaded_sample.txt"

# Initialize the S3 client using credentials from `aws configure`
s3 = boto3.client("s3")


def list_buckets():
    print("\n--- 1. Listing S3 Buckets ---")
    response = s3.list_buckets()
    for bucket in response["Buckets"]:
        print(f" - {bucket['Name']}")


def upload_file(local_path, bucket, s3_key):
    print(f"\n--- 2. Uploading '{local_path}' to s3://{bucket}/{s3_key} ---")
    s3.upload_file(
        local_path,
        bucket,
        s3_key,
        ExtraArgs={"Metadata": {"author": "Jay-Adithya", "project": "S3-Cloud-Storage"}}
    )
    print("Upload successful.")


def list_bucket_objects(bucket):
    print(f"\n--- 3. Listing Objects in '{bucket}' ---")
    response = s3.list_objects_v2(Bucket=bucket)
    for obj in response.get("Contents", []):
        print(f" - {obj['Key']} ({obj['Size']} bytes)")


def extract_metadata(bucket, s3_key):
    print(f"\n--- 4. Extracting Metadata for '{s3_key}' ---")
    response = s3.head_object(Bucket=bucket, Key=s3_key)
    print(f" Content-Type  : {response['ContentType']}")
    print(f" Content-Length: {response['ContentLength']} bytes")
    print(f" Last Modified : {response['LastModified']}")
    print(f" ETag          : {response['ETag']}")
    print(f" Custom Meta   : {response['Metadata']}")


def download_file(bucket, s3_key, download_path):
    print(f"\n--- 5. Downloading '{s3_key}' to '{download_path}' ---")
    s3.download_file(bucket, s3_key, download_path)
    print("Download successful.")


if __name__ == "__main__":
    try:
        # Skipping list_buckets() due to AWS Organization SCP restriction
        upload_file(LOCAL_FILE, BUCKET_NAME, S3_KEY)
        list_bucket_objects(BUCKET_NAME)
        extract_metadata(BUCKET_NAME, S3_KEY)
        download_file(BUCKET_NAME, S3_KEY, DOWNLOAD_PATH)
    except ClientError as e:
        print(f"AWS Error: {e}")