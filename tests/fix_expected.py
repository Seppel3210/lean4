#!/usr/bin/env python3

import argparse
import os
import subprocess
from pathlib import Path

# Run in repo root
os.chdir(Path(__file__).parent.parent)


parser = argparse.ArgumentParser(
    description="Interactively fix *.expected files "
    "based on their corresponding *.produced files."
)
args = parser.parse_args()


def compare_and_fix(expected_file: Path, produced_file: Path) -> None:
    if not produced_file.exists():
        print(f"{expected_file}: No corresponding {produced_file}")
        return

    expected = expected_file.read_bytes()
    produced = produced_file.read_bytes()

    if expected == produced:
        return

    print(f"{expected_file}: Differs from {produced_file}")

    # This is the opposite direction of the tests' diff output, but meld puts
    # the cursor into the right file by default, and only saves the file with
    # the cursor when pressing Ctrl+S, so this order is more convenient for
    # quickly fixing many files.
    subprocess.run(["meld", produced_file, expected_file])


for expected_file in Path().rglob("*.expected"):
    produced_file = expected_file.with_suffix(".produced")
    compare_and_fix(expected_file, produced_file)

# Old file naming scheme

for expected_file in Path().rglob("*.expected.out"):
    produced_file = expected_file.with_suffix("").with_suffix(".produced.out")
    compare_and_fix(expected_file, produced_file)

for expected_file in Path().rglob("*.expected.ret"):
    produced_file = expected_file.with_suffix("").with_suffix(".produced.ret")
    compare_and_fix(expected_file, produced_file)
