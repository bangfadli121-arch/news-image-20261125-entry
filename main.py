#!/usr/bin/env python3
"""Koran 25 entry program (stdlib only).

Copies the bundled entry.png to /output/entry.png. No network, no
third-party imports, deterministic: the same bytes out on every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT = "/output/entry.png"


def main():
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, OUT)


if __name__ == "__main__":
    main()
