import boto3
from botocore.client import Config

MINIO_ENDPOINT = "http://localhost:9000"
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "password123"
BUCKET_NAME = "my-bucket"

def get_client():
    return boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        config=Config(signature_version="s3v4"),
    )

def main():
    client = get_client()

    # Create bucket if it doesn't exist
    existing_buckets = [b["Name"] for b in client.list_buckets().get("Buckets", [])]
    if BUCKET_NAME not in existing_buckets:
        client.create_bucket(Bucket=BUCKET_NAME)
        print(f"Bucket '{BUCKET_NAME}' created.")
    else:
        print(f"Bucket '{BUCKET_NAME}' already exists.")

    # Upload a file
    client.put_object(Bucket=BUCKET_NAME, Key="hello.txt", Body=b"Hello from MinIO!")
    print("File 'hello.txt' uploaded.")

    # List objects in bucket
    response = client.list_objects_v2(Bucket=BUCKET_NAME)
    print("Objects in bucket:")
    for obj in response.get("Contents", []):
        print(f"  - {obj['Key']} ({obj['Size']} bytes)")

    # Download and print file content
    obj = client.get_object(Bucket=BUCKET_NAME, Key="hello.txt")
    print("Content of 'hello.txt':", obj["Body"].read().decode())


if __name__ == "__main__":
    main()

