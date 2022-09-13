import os


def build():
    name = "rfgui"

    if os.path.exists(f"dist/{name}.exe"):
        override = input("WARNING: You are about to override an existing file. Proceed? (Y/n) ") == "Y"

        if not override:
            print("Quitting...")
            quit(-1)
        else:
            print("Deleting existing file...")
            os.remove(f"dist/{name}.exe")

    print(f"Building {name}.exe")
    os.system(f"pyinstaller --onefile dev/{name}.py")

if __name__ == '__main__':
    build()