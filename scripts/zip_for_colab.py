"""
Zip a processed dataset for upload to Google Colab via Google Drive.

Usage:
    python scripts/zip_for_colab.py --dataset combined
    python scripts/zip_for_colab.py --dataset visdrone
    python scripts/zip_for_colab.py --dataset uavdt
"""

import argparse
import io
import os
import sys
import zipfile
from pathlib import Path

import yaml
from tqdm import tqdm

REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_ROOT = REPO_ROOT / "data" / "processed"
OUTPUT_DIR = REPO_ROOT / "colab_uploads"

VALID_DATASETS = ("combined", "visdrone", "uavdt")
COLAB_DATASET_PATH = "/content/dataset"


def parse_args():
    parser = argparse.ArgumentParser(description="Zip a processed dataset for Colab upload.")
    parser.add_argument(
        "--dataset",
        choices=VALID_DATASETS,
        required=True,
        help="Which dataset to zip: combined, visdrone, or uavdt",
    )
    return parser.parse_args()


def validate_source(src: Path):
    if not src.exists():
        print(f"ERROR: Source directory not found: {src}")
        sys.exit(1)
    all_files = list(src.rglob("*"))
    data_files = [f for f in all_files if f.is_file()]
    if not data_files:
        print(f"ERROR: Source directory is empty: {src}")
        sys.exit(1)
    return data_files


def confirm_overwrite(zip_path: Path) -> bool:
    print(f"Zip already exists: {zip_path}")
    answer = input("Overwrite? (yes/no): ").strip().lower()
    return answer in ("yes", "y")


def rewrite_yaml_for_colab(yaml_path: Path) -> bytes:
    """Read the dataset yaml and return modified bytes with path rewritten for Colab."""
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    data["path"] = COLAB_DATASET_PATH
    return yaml.dump(data, default_flow_style=False).encode("utf-8")


def zip_dataset(src: Path, zip_path: Path, dataset: str):
    data_files = validate_source(src)

    # Collect all files and compute arcnames (relative to src root)
    entries = []
    yaml_path = None
    for f in data_files:
        rel = f.relative_to(src)
        arcname = str(rel)
        if f.suffix == ".yaml":
            yaml_path = f
        entries.append((f, arcname))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if zip_path.exists():
        if not confirm_overwrite(zip_path):
            print("Aborted.")
            sys.exit(0)

    print(f"Zipping {len(entries)} files from {src} → {zip_path}")

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path, arcname in tqdm(entries, unit="file", desc="Zipping"):
            if yaml_path and file_path == yaml_path:
                # Write the Colab-rewritten yaml in place of the original
                colab_yaml_bytes = rewrite_yaml_for_colab(file_path)
                zf.writestr(arcname, colab_yaml_bytes)
            else:
                zf.write(file_path, arcname)

    size_gb = zip_path.stat().st_size / (1024 ** 3)
    print(f"Done. Zip size: {size_gb:.3f} GB")
    print(f"Output: {zip_path}")


def main():
    args = parse_args()
    dataset = args.dataset
    src = PROCESSED_ROOT / f"{dataset}_yolo"
    zip_path = OUTPUT_DIR / f"{dataset}_yolo.zip"
    zip_dataset(src, zip_path, dataset)


if __name__ == "__main__":
    main()
