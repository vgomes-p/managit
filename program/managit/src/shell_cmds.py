import managit.src.shells_prompt as PRMT
from managit.utils.colors import DEFAULT
import os


def get_current_path():
    return os.getcwd()


def handle_cd(new_path: str):
    if new_path == "cd":
        print(f"{PRMT.ERR} 'cd' needs a path")
        return
    if "cd " in new_path:
        new_path = new_path.replace("cd ", '')
    if "cd" in new_path:
        new_path = new_path.replace("cd", '')
    if "~" in new_path:
        try:
            os.chdir("~")
        except:
            print(f"{PRMT.ERR} not able to reach home!{DEFAULT}")
        return
    try:
        current = get_current_path()
        new_path = f"{current}/{new_path}"
        os.chdir(new_path)
    except:
        print(f"{PRMT.ERR} not able to reach '{new_path}'!{DEFAULT}")


def check_dir_exits(entry: str):
    if entry == "~":
        return True
    dirs_at_path = os.listdir(".")
    if "\\" in entry:
        entry = entry.replace("\\", "/")
    if "/" in entry:
        entry_ls = entry.split("/")
        entry_ls.pop(0)
    else:
        entry_ls = [entry]
    to_check = entry_ls[0]
    if to_check in dirs_at_path:
        return True
    return False


def run_ls(path: str = "."):
    to_list = path
    try:
        listdir_ret = os.listdir(to_list)
    except OSError as e:
        print(f"{PRMT.ERR} Not able to access path '{to_list}': {e}{DEFAULT}")
        return
    cnt = 0
    for i in listdir_ret:
        if os.path.isdir(i):
            print(f"{i}/", end="")
        else:
            print(i, end="")
        cnt += 1
        if cnt <= (len(listdir_ret) - 1):
            print(", ", end="")
    print("")


def handle_ls(entry: str):
    f_entry = entry.replace("ls ", "").replace("ls", "")
    if "-" in f_entry:
        print(f"{PRMT.ERR} ls flags are not implemented!{DEFAULT}")
    elif f_entry == "~":
        print(f"{PRMT.ERR} enter a valid path!{DEFAULT}")
    elif f_entry:
        run_ls(f_entry)
    else:
        run_ls()


def cnt_pipes(entry: str):
    pipes = ["|", "&&"]
    s_entry = entry.split()
    pipe_cnt = 0
    for p in pipes:
        for e in s_entry:
            pipe_cnt += 1 if e == p else 0
    return pipe_cnt
