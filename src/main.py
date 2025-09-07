import os
import shutil
import sys
from generate_pages import generate_pages_recursive

def update_static():
    
    directory = os.listdir("docs")
    for file in directory:
        if os.path.isfile(f"docs/{file}"):
            os.remove(f"docs/{file}")
        else:
            shutil.rmtree(f"docs/{file}")
    directory = os.listdir("static")
    shutil.copytree("static", "docs", dirs_exist_ok=True)
    

def main():
    update_static()
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    generate_pages_recursive("content", "template.html", "docs", basepath)




main()

