import os
import stat
import shutil
import subprocess

extensions = [".txt", ".md", ".jpg", ".jpeg", ".png"]

# remove directory with read-only files
def rmdir_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def get_size(path):
    return int(subprocess.check_output(['du','-s', path]).split()[0].decode('utf-8'))

def main():
    files = directories = []
    try:
        files = os.environ["FILES"][1:-1]
        files = [f.strip() for f in files.split(',')]
        ext = [f for f in files if (f in extensions)]
        for f in files:
            if f in ext:
                files.remove(f)
    except:
        print("No files on input.")

    try:
        directories = os.environ["DIRECTORIES"][1:-1]
    except:
        print("No directories on input.")

    cwd = os.getcwd()
    init_size = get_size(cwd)

    # TODO: Before removing the file, check if it is referenced in any executable file
    for root,dirs,fs in os.walk(cwd):
        for d in dirs:
            if d in directories:
                shutil.rmtree(d, onerror=rmdir_readonly)
                print(f"Removing directory {d}")
        for f in fs:
            if f in files or f.endswith(tuple(ext)):
                os.remove(f)
                print(f"Removing file {f}")

    final_size = get_size(cwd)
    size_ratio = 1 - final_size/init_size

    print(f"Output image size reduced for {size_ratio}")


if __name__ == '__main__':
    main()
