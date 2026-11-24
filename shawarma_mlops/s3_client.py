import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import subprocess
from typing import Any

import boto3
from botocore.config import Config
from botocore import UNSIGNED

from shawarma_mlops.config import METADATA_PATH

BASE_URL = "https://itudsip.hel1.your-objectstorage.com/data"

# S3 Configuration for Hetzner
S3_ENDPOINT = "https://itudsip.hel1.your-objectstorage.com"
S3_BUCKET = "data"


class S3Client:
    _client: Any  # boto3 client. the package does not provide type hints

    def __init__(self) -> None:
        self._client = boto3.client(
            's3',
            endpoint_url=S3_ENDPOINT,
            aws_access_key_id='',
            aws_secret_access_key='',
            config=Config(signature_version=UNSIGNED)
        )

    @classmethod
    def get_s3_key_from_url(cls, url: str) -> str:
        """
        URL format: https://itudsip.hel1.your-objectstorage.com/data/images/metadata.csv
        Bucket: data, Key: images/metadata.csv
        """
        return url.replace(f"{S3_ENDPOINT}/{S3_BUCKET}/", "")

    def _download_file_with_boto3(self, key: str, output_path: Path) -> bool:
        """Download a single file from S3 using boto3."""
        if output_path.exists():
            return False
        try:
            # because download_file is a method that is dynamically added to the client,
            # we need to ignore type checking for this line
            self._client.download_file(S3_BUCKET, key, str(output_path))
            return True
        except Exception as e:
            print(f"Failed to download {key}: {e}")
            return False

    def download_with_dvc(self, url: str, out_path: Path) -> None:
        """Download a single file (DVC-compatible interface)."""
        if out_path.exists():
            print(f"File {out_path} already exists, skipping download")
            return
        key = self.get_s3_key_from_url(url)
        self._client.download_file(S3_BUCKET, key, str(out_path))
        print(f"Downloaded {url} to {out_path}")

    def download_files_from_metadata(self, metadata_path: Path, output_dir: Path, prefix: str = "") -> None:
        """Download all files listed in a metadata csv from the object store."""
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(metadata_path) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        downloaded_count = 0
        skipped_count = 0
        failed_count = 0

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {}
            for row in rows:
                filename = row["filename"]
                key = f"{prefix}{filename}"
                output_path = output_dir / filename
                future = executor.submit(self._download_file_with_boto3, key, output_path)
                futures[future] = (key, output_path)

            for future in as_completed(futures):
                key, output_path = futures[future]
                if future.result():
                    downloaded_count += 1
                else:
                    if output_path.exists():
                        skipped_count += 1
                    else:
                        failed_count += 1

        print(f"Downloaded {downloaded_count} images, skipped {skipped_count} existing, failed {failed_count}")

    def pull_data_from_dvc(self) -> None:
        """Pull the training and test images listed in the metadata from the object store."""
        dvc_pull_result = subprocess.run(["dvc", "pull"], capture_output=True, text=True)
        if dvc_pull_result.returncode != 0:
            print(f"DVC pull failed: {dvc_pull_result.stderr}")
            raise RuntimeError("DVC pull failed")

        self.download_files_from_metadata(METADATA_PATH, Path("data/images/raw"), "images/raw/")
        self.download_files_from_metadata(METADATA_PATH, Path("data/test"), "test/")

