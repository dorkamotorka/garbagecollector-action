import os
import stat
import shutil
import subprocess

extensions = ["*.txt", "*.md", "*.jpg", "*.jpeg", "*.png"]

# remove directory with read-only files
def rmdir_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def get_size(path):
    return int(subprocess.check_output(['du','-s', path]).split()[0].decode('utf-8'))

def main():
    files = directories = []
    try:
        files = os.environ["INPUT_FILES"][1:-1]
        files = files.split(",")
        ext = [f.strip() for f in files if (f.strip() in extensions)]
        directories = os.environ["INPUT_DIRECTORIES"]
    except:
        print("No input defined, nothing will be removed")
    
    cwd = os.getcwd()
    init_size = get_size(cwd)

    # TODO: Before removing the file, check if it is referenced in any executable file
    for root,dirs,fs in os.walk(cwd):
        for d in dirs:
            if d in directories:
                shutil.rmtree(d, onerror=rmdir_readonly)
        for f in fs:
            if f in files or f.endswith(tuple(ext)):
                os.remove(f)

    final_size = get_size(cwd)
    size_ratio = 1 - final_size/init_size

    print(f"::set-output name=size::{size_ratio}")


if __name__ == '__main__':
    main()
