import os
import sys
import datetime
from send_emails import send_emails

# Get filepath of comic
filepath = input("Please input filepath: ")

# Get custom date if user wants to
today = input("Custom date (leave blank to use today) (MM-DD-YYYY, no zero-padding) ")

if not today:
    # Get today's date
    today = datetime.date.today().strftime('%#m-%#d-%Y')

# Get comic format
_, format = os.path.splitext(filepath)
format = format.lower()
format = format.replace('.', '', 1)

if format not in ("jpeg", "jpg", "png", "svg", "webp"):
    print(f"WARNING: File format may be unsupported. Website functionality may break. Recommended file formats: JPEG (JPG), PNG, SVG, WEBP. Your file format: {format.upper()}")
    format_override = input("Proceed? (y/N)") == 'y'

    if not format_override: sys.exit(1)



# If the filepath doesn't exist, warn the user and quit the application
if not os.path.exists(filepath):
    print("FATAL: Filepath does not exist. Please confirm sure that there are no typos and that the file actually exists.")
    sys.exit(1)

if os.path.exists(f"comics/{today}.{format}"):
    override = input("WARNING: You are about to override today's comic. Proceed? (Y/n): ") == 'Y'

    if not override: sys.exit(1)
else:
    override = False

# Read comic from original filepath
print(f"Reading binary from {filepath}...")
with open(filepath, 'rb') as f:
    raw_comic = f.read()


# Write comic to comics directory
print(f"Writing binary to dev/comics/{today}.{format}...")
with open(f"dev/comics/{today}.{format}", 'wb') as f:
    f.write(raw_comic)


# We don't want to update comic_num if there is a file override
if not override:
    # Update comic_num.txt

    print("Updating statistics...")
    with open("dev/comic_num.txt", 'r+') as f:
        prev_comic_num = int(f.read())
        comic_num = prev_comic_num + 1

        f.seek(0)
        f.write(str(comic_num))
else:
    with open("dev/comic_num.txt", 'r') as f:
        comic_num = int(f.read())


# Commit and push to GitHub #

print("\nStaging changes...")
os.system("git add .")

print("\nCommitting...")
os.system(f'git commit -m "Automatic Daily Comic upload #{comic_num}"')

print("\nPulling...")
os.system("git pull https://github.com/RichestFinest/richestfinest.github.io master")

print("\nPushing...")
os.system('git push https://github.com/RichestFinest/richestfinest.github.io master')

print("\nCommit and push completed.")

print("\nSending notifications to subscribers...")
send_emails(f"dev/comics/{today}.{format}")

print("\nUpload suite completed.")



