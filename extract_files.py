import os
import zipfile
from pathlib import Path


def extract_zip(zip_path, extract_path):
    Path(extract_path).mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

        os.remove(zip_path)
