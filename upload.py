import os
import sys
import datetime

# Get filepath of comic
filepath = input("Please input filepath: ")

# Get comic format
_, format = os.path.splitext(filepath)
format = format.lower()
format = format.replace('.', '')

if format not in ("jpeg", "jpg", "png", "svg", "webp"):
    print(f"WARNING: File format may be unsupported. Recommended file formats: JPEG (JPG), PNG, SVG, WEBP. Your file format: {format.upper()}")
    override = input("To override warning and continue, input 'O'. To quit, leave blank and enter.") == 'O'

    if not override: sys.exit(1)

# Get today's date
today = datetime.date.today().strftime('%Y-%m-%d')

# If the filepath doesn't exist, warn the user and quit the application
if not os.path.exists(filepath):
    print("FATAL: Filepath does not exist. Please confirm sure that there are no typos and that the file actually exists.")
    sys.exit(1)

if os.path.exists(f"comics/{today}.{format}"):
    override = input("WARNING: You are about to override today's comic. Proceed? (Y/n): ") == 'Y'

    if not override: sys.exit(1)

# Read comic from original filepath
with open(filepath, 'rb') as f:
    raw_comic = f.read()

# Write comic to comics directory
with open(f"comics/{today}.{format}", 'wb') as f:
    f.write(raw_comic)

# TODO: ADD GIT STUFF
