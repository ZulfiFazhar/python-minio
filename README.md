# Python MinIO

A minimal Python application that demonstrates how to connect to a [MinIO](https://min.io/) object storage server using `boto3` (AWS S3-compatible API). MinIO runs locally via Docker Compose.

## Overview

This project shows how to:

- Spin up a MinIO instance with Docker Compose
- Connect to MinIO from Python using `boto3`
- Create a bucket
- Upload an object
- List objects in a bucket
- Download and read an object

## Project Structure

```
minio/
├── data/                  # MinIO persistent storage (auto-created)
├── docker-compose.yml     # MinIO service definition
├── main.py                # Python demo script
├── pyproject.toml         # Project metadata and dependencies
└── README.md
```

## Prerequisites

- [Python](https://www.python.org/) >= 3.10
- [Docker](https://www.docker.com/) with Compose plugin (or Docker Desktop)
- [uv](https://docs.astral.sh/uv/) or `pip` for Python dependency management

## Getting Started

### 1. Start MinIO

```bash
docker compose up -d
```

This starts two services on:
| Port | Purpose |
|------|---------|
| `9000` | S3 API endpoint |
| `9001` | Web console (MinIO UI) |

Verify the container is running:

```bash
docker compose ps
```

### 2. Install Python Dependencies

Using `uv` (recommended):

```bash
uv sync
```

Or using `pip`:

```bash
pip install boto3
```

### 3. Run the App

```bash
python main.py
```

Expected output:

```
Bucket 'my-bucket' created.
File 'hello.txt' uploaded.
Objects in bucket:
  - hello.txt (17 bytes)
Content of 'hello.txt': Hello from MinIO!
```

## Configuration

Credentials and endpoints are defined at the top of [main.py](main.py):

```python
MINIO_ENDPOINT   = "http://localhost:9000"
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "password123"
BUCKET_NAME      = "my-bucket"
```

These match the environment variables in [docker-compose.yml](docker-compose.yml):

```yaml
MINIO_ROOT_USER: admin
MINIO_ROOT_PASSWORD: password123
```

> **Note:** Change these credentials before deploying to any non-local environment.

## MinIO Web Console

Once the container is running, open the MinIO web UI at:

```
http://localhost:9001
```

Login with `admin` / `password123` to browse buckets and objects visually.

## How the boto3 Connection Works

MinIO is S3-compatible, so `boto3` works out of the box by pointing `endpoint_url` to the local MinIO server instead of AWS:

```python
import boto3
from botocore.client import Config

client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",   # MinIO instead of AWS
    aws_access_key_id="admin",
    aws_secret_access_key="password123",
    config=Config(signature_version="s3v4"), # required by MinIO
)
```

## Stopping MinIO

```bash
docker compose down
```

Data is persisted in `./data/` and will be available on the next `docker compose up`.
To also remove stored data:

```bash
docker compose down
Remove-Item -Recurse -Force .\data   # PowerShell
# or
rm -rf ./data                        # bash/WSL
```
