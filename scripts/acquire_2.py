#!/usr/bin/env python3
"""
Script to download a zip file from a URL and extract its contents to a Google Cloud Storage bucket.

Requirements:
    pip install google-cloud-storage requests

Usage:
    python download_and_extract_to_gcs.py
"""

import os
import io
import zipfile
import requests
from google.cloud import storage

from typing import Optional
import sys


def download_and_extract_to_gcs(
        zip_url: str,
        bucket_name: str,
        destination_prefix: str = "",
        staging_dir: str = ""
) -> None:
    """
    Download a zip file from a URL and extract its contents to a GCS bucket.

    Args:
        zip_url: URL of the zip file to download
        bucket_name: Name of the GCS bucket
        destination_prefix: Optional prefix/folder path in the bucket (e.g., "extracted/")
    """

    # Download the zip file
    print(f"Downloading zip file from: {zip_url}")
    try:
        response = requests.get(zip_url, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        sys.exit(1)

    # Read the zip file into memory
    zip_content = io.BytesIO(response.content)
    print(f"Download complete. File size: {len(response.content) / (1024 * 1024):.2f} MB")

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    print(f"Extracting files to GCS bucket: {bucket_name}")

    # Extract and upload files
    uploaded_count = 0
    with zipfile.ZipFile(zip_content, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        total_files = len(file_list)

        print(f"Found {total_files} files in the archive")

        for file_name in file_list:
            # Skip directories
            if file_name.endswith('/'):
                continue

            # Extract file from zip
            zip_ref.extract(file_name, staging_dir)
            local_file = os.path.join(staging_dir, file_name)
            print(f"Unzipping to {local_file}...")

            # Construct the destination path in GCS
            if destination_prefix:
                # Ensure prefix ends with /
                prefix = destination_prefix.rstrip('/') + '/'
                gcs_path = prefix + file_name
            else:
                gcs_path = file_name

            # Upload to GCS
            blob = bucket.blob(gcs_path)
            blob.upload_from_filename(local_file)
            uploaded_count += 1
            print(f"[{uploaded_count}/{total_files}] Uploaded: {gcs_path}")

            # Delete the staged file
            os.remove(local_file)
            print(f"Deleted")

    print(f"\n✓ Successfully extracted {uploaded_count} files to gs://{bucket_name}/{destination_prefix}")


def main():
    """
    Main function with example usage.
    Modify these variables for your use case.
    """

    # Configuration
    ZIP_URL = "https://www.sciencebase.gov/catalog/file/get/56d07d9de4b015c306ee988c?f=__disk__c0%2Fd8%2F47%2Fc0d8474b60e01f3e81b2e388b320a14a4dd623f9"  # URL of the zip file
    BUCKET_NAME = "grousemapper_raw"  # Your GCS bucket name
    DESTINATION_PREFIX = "suitability_layer/"  # Optional: folder path in bucket (use "" for root)
    STAGING_DIR = r"D:\staging"

    # Run the extraction
    download_and_extract_to_gcs(
        zip_url=ZIP_URL,
        bucket_name=BUCKET_NAME,
        destination_prefix=DESTINATION_PREFIX,
        staging_dir=STAGING_DIR
    )



if __name__ == "__main__":
    main()
