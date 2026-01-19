"""
download_uavdt.py

Purpose:
This script documents and verifies the UAVDT (UAV Detection and Tracking)
dataset dependency.

Due to the large size of the dataset, UAVDT is not stored in this GitHub
repository. Instead, users are instructed to download the dataset from
the official Zenodo release and place it in the expected directory.

Official source:
https://zenodo.org/records/14575517
"""

from pathlib import Path
import sys

# Expected dataset location
UAVDT_DIR = Path("data/raw/uavdt")

def main():
    print("UAVDT Dataset Setup")
    print("-" * 40)

    if UAVDT_DIR.exists():
        print(f"UAVDT dataset found at: {UAVDT_DIR.resolve()}")
        print("Dataset is available and ready for use.")
    else:
        print("UAVDT dataset not found.")
        print()
        print("Please download the UAVDT dataset from the Zenodo release:")
        print("https://zenodo.org/records/14575517")
        print()
        print("Download the ZIP file and extract it so that the directory")
        print("structure looks like this:")
        print()
        print("data/raw/uavdt/")
        print("├── images/           # UAVDT image frames")
        print("├── annotations/      # bounding box annotations")
        print("└── README or metadata files")
        print()
        print("After extracting the dataset, re-run this script.")
        sys.exit(1)

if __name__ == "__main__":
    main()