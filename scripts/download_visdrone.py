"""
download_visdrone.py

Purpose:
This script documents and verifies the VisDrone dataset dependency.

Due to the large size of the dataset, VisDrone is not stored directly
in this GitHub repository. Instead, users are instructed to download
the dataset from the official source and place it in the expected
directory structure.

Official source:
https://github.com/VisDrone/VisDrone-Dataset
"""

from pathlib import Path
import sys

# Expected dataset location
VISDRONE_DIR = Path("data/raw/visdrone")

def main():
    print("VisDrone Dataset Setup")
    print("-" * 40)

    if VISDRONE_DIR.exists():
        print(f"VisDrone dataset found at: {VISDRONE_DIR.resolve()}")
        print("Dataset is available and ready for use.")
    else:
        print("VisDrone dataset not found.")
        print()
        print("Please download the VisDrone Detection dataset from:")
        print("https://github.com/VisDrone/VisDrone-Dataset")
        print()
        print("After downloading, extract the dataset so that the directory")
        print("structure matches the following:")
        print()
        print("data/raw/visdrone/")
        print("├── VisDrone2019-DET-train/")
        print("├── VisDrone2019-DET-val/")
        print("└── VisDrone2019-DET-test-dev/")
        print()
        print("Once extracted, re-run this script.")
        sys.exit(1)

if __name__ == "__main__":
    main()