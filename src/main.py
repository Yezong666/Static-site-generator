import os
import shutil
import sys
from generate_pages import generate_pages_recursive

def update_static():
    
    directory = os.listdir("public")
    for file in directory:
        if os.path.isfile(f"public/{file}"):
            os.remove(f"public/{file}")
        else:
            shutil.rmtree(f"public/{file}")
    directory = os.listdir("static")
    shutil.copytree("static", "public", dirs_exist_ok=True)
    

def main():
    update_static()
    basepath = "/"
    if len(sys.argv) > 0:
        basepath = sys.argv[0]
    
    generate_pages_recursive("content", "template.html", "docs", basepath)




main()

