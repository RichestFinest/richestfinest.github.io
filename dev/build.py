import os


def build():
    if os.path.exists(f"dist/rfgui.exe"):
        override = input("WARNING: You are about to override an existing file. Proceed? (Y/n) ") == "Y"

        if not override:
            print("Quitting...")
            quit(-1)
        else:
            print("Deleting existing file...")
            os.remove(f"dist/rfgui.exe")

    print(f"Building rfgui.exe")
    os.system(f"pyinstaller --onefile dev/rfgui.py")

    with open("dist/rfgui.exe", 'rb') as f:
        file = f.read()

    with open("rfgui.exe", 'wb') as f:
        f.write(file)

    os.remove("dist/rfgui.exe")

    print(f"Built sucessfully! rfgui.exe can be found here: {os.path.abspath('rfgui.exe')}")


if __name__ == '__main__':
    build()