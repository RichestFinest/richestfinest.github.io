import os
from build import build

def update():
    print("Pulling from remote repository...")
    os.system("git pull https://github.com/RichestFinest/richestfinest.github.io master")

    