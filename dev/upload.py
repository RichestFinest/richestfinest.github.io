import os
import datetime
from send_emails import send_emails
import errors

# Get filepath of comic
# filepath = input("Please input filepath: ")

# Get custom date if user wants to
# today = input("Custom date (leave blank to use today) (MM-DD-YYYY, no zero-padding) ")

def upload(filepath, date=None, override=False):
    if not date:
        # Get today's date
        date = datetime.date.today().strftime('%#m-%#d-%Y')

    # Get comic format
    _, format = os.path.splitext(filepath)
    format = format.lower()
    format = format.replace('.', '', 1)

    if format not in ("jpeg", "jpg", "png", "svg", "webp"):
        raise TypeError("File format invalid: must be a supported image format. (jpg, png, svg, webp)")

    # If the filepath doesn't exist, warn the user and quit the application
    if not os.path.exists(filepath):
        raise TypeError("Filepath does not exist. Please confirm sure that there are no typos and that the file actually exists.")

    if os.path.exists(f"comics/{date}.{format}") and not override:
        raise errors.OverrideWarning("File already exists. To override, run upload() with override=True.")

    # Read comic from original filepath
    print(f"Reading binary from {filepath}...")
    with open(filepath, 'rb') as f:
        raw_comic = f.read()


    # Write comic to comics directory
    print(f"Writing binary to dev/comics/{date}.{format}...")
    with open(f"dev/comics/{date}.{format}", 'wb') as f:
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
    send_emails(f"dev/comics/{date}.{format}")

    print("\nUpload suite completed.")



