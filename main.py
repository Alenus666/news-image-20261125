"""make.fun entry: write the 25 November 2026 world-news image to /output/entry.png.

The image is rendered ahead of time by make_image.py and stored in assets/.
This program only copies it, so it needs no network and every run writes
the same bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assets", "entry.png")
OUT_DIR = os.environ.get("OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SRC, os.path.join(OUT_DIR, "entry.png"))
