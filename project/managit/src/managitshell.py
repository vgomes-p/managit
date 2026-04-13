from managit.utils.clear import clear
from managit.utils.colors import CYAN, DEFAULT, RED, YLOW, PINK, GREEN, BOLD
from managit.src.get_commit_info import get_commit_info
from contextlib import contextmanager
from time import sleep
import subprocess
import signal
import os

init_txt = CYAN + """┌──────────────────────────────────────────────────────────────────┐
│╔════════════════════════════════════════════════════════════════╗│
│║ ██      ██  ██████  ██   ██  ██████  ███████  ██████  ████████ ║│
│║ ██████████  ██  ██  ███  ██  ██  ██  ██         ██       ██    ║│
│║ ██  ██  ██  ██████  ██ █ ██  ██████  ██ ████    ██       ██    ║│
│║ ██      ██  ██  ██  ██  ███  ██  ██  ██   ██    ██       ██    ║│
│║ ██      ██  ██  ██  ██   ██  ██  ██  ███████  ██████     ██    ║│
│╚════════════════════════════════════════════════════════════════╝│
│                   made by github.com/vgomes-p                    │
└──────────────────────────────────────────────────────────────────┘""" + DEFAULT

def get_current_path():
    return os.getcwd()

def get_pathsumup(path: str):
    if '\\' in path:
        path = path.replace('\\', '/')
    splited_path = path.split('/')
    sumup_ls = ['~/']
    if len(splited_path) >= 4 and splited_path[-1] != '':
        for i in range(1 ,len(splited_path)):
            sumup_ls.append(f"{splited_path[i][0]}/")
    if len(sumup_ls) <= 3:
        dircnt = 0
    else:
        sumup_ls.pop(-1)
        sumup_ls.pop(1)
        sumup_ls.pop(1)
        dircnt = len(sumup_ls)
    sumup_ls.append(f"({dircnt}){splited_path[-1]}")
    return "".join(sumup_ls)

def get_user():
    return os.getenv("USER")

shell, shell_att, shell_err, usershell = "", "", "", ""

def update_shellsname(path: str):
    global shell, shell_att, shell_err, usershell
    username = get_user()
    paths = get_pathsumup(path)
    shell = f"{CYAN}managit@{paths} $ {DEFAULT}{BOLD}"
    shell_att = f"{CYAN}managit@{paths} ${YLOW} ATTENTION:"
    shell_err = f"{CYAN}managit@{paths} ${RED} ERROR:"
    usershell = f"{CYAN}{username}@{paths} $ {DEFAULT}{BOLD}"

def get_pull(path: str):
    fpath = os.path.expanduser(path)
    try:
        ord = ["git", "pull"]
        subprocess.run(ord, cwd=fpath, check=True, capture_output=True)
        print("Updates pulled!")
    except FileNotFoundError:
        print(f"{YLOW}No .git was found in the current path {PINK}'{path}'!{DEFAULT}")
    except OSError as e:
        print(f"{RED}Error on accessing the repository directory: {e}{DEFAULT}")


def handle_pull(path: str):
    fpath = os.path.expanduser(path)
    print(f"{shell}checking if pulling is necessary...")
    sleep(.5)
    try:
        ord = ["git", "rev-list", "--count", "HEAD..origin/HEAD"]
        ret = subprocess.run(ord, cwd=fpath, check=True, capture_output=True)
        behind = int(ret.stdout.strip())
        if behind > 0:
            print(f"{shell}Pulling is needed. Starting pulling...")
            sleep(.5)
            print(get_pull())
        else:
            print(f"{shell}Nothing to pull!")
    except FileNotFoundError:
        print(f"{shell_att}No .git was found in the current path {PINK}'{path}'!{DEFAULT}")
    except OSError as e:
        print(f"{shell_err}Error on accessing the repository directory: {e}{DEFAULT}")


def mk_add(path: str):
    fpath = os.path.expanduser(path)
    try:
        ord = ["git", "add", "."]
        subprocess.run(ord, cwd=fpath, check=True, capture_output=True)
    except FileNotFoundError:
        print(f"{YLOW}No .git was found in the current path {PINK}'{path}'!{DEFAULT}")
    except OSError as e:
        print(f"{shell_err}Error on accessing the repository directory: {e}{DEFAULT}")


def mk_commit(path: str, commit_text: str, other_text: list = []):
    fpath = os.path.expanduser(path)
    try:
        ord = ["git", "commit", "-m"]
        ord.append(commit_text)
        for i in other_text:
            ord.append("-m")
            ord.append(i)
        subprocess.run(ord, cwd=fpath, check=True, capture_output=True)
    except FileNotFoundError:
        print(f"{YLOW}No .git was found in the current path {PINK}'{path}'!{DEFAULT}")
    except OSError as e:
        print(f"{shell_err}Error on accessing the repository directory: {e}{DEFAULT}")


def handle_commit(path: str):
    cmt_text, ocmt_ls = get_commit_info()
    if cmt_text == "canceled":
        return
    print(f"{shell}Adding files from {path} to commit...")
    sleep(.3)
    mk_add(path)
    print(f"{shell}Starting the commit informations system")
    sleep(.5)
    print(f"{shell}Creating commit text...")
    sleep(.4)
    print(f"{shell}Commiting to git repository...")
    mk_commit(path, cmt_text, ocmt_ls)


def mk_push(path: str, force: bool = False):
    try:
        if force:
            ord = ["git", "push", "--force"]
        else:
            ord = ["git", "push"]
        subprocess.run(ord, check=True, capture_output=True)
    except FileNotFoundError:
        print(f"{YLOW}No .git was found in the current path {PINK}'{path}'!{DEFAULT}")


def handle_push(path):
    print(f"{shell}Do you want to force push? ['y' for yes, 'n' for no]")
    while True:
        check = input(usershell).lower() + DEFAULT
        if check == "cancel":
            return
        elif check == 'y':
            mk_push(path, force=True)
            break
        elif check == 'n':
            mk_push(path, force=False)
            break
        else:
            print(f"{shell}please, answer 'y' for yes or 'n' for no!")
            continue
    print(f"{shell}everything was pushed!")


def mk_new_branch(path: str, branch_name: str, base_branch: str):
    fpath = os.path.expanduser(path)
    ord = ["git", "checkout", "-b", branch_name, base_branch]
    try:
        subprocess.run(ord, cwd=fpath, check=True, capture_output=True)
    except FileNotFoundError:
        print(f"{YLOW}No .git was found in the current path {PINK}'{path}'!{DEFAULT}")
    except OSError as e:
        print(f"{shell_err}Error on accessing the repository directory: {e}{DEFAULT}")


def handle_new_branch(path):
    while True:
        branch_name = input(f"{shell}What's the new branch name?\n{usershell}") + DEFAULT
        print(f"The new branch name will be '{branch_name}'. Confirm that? ['y' for yes, 'c' or 'n' to change the name]")
        conf = input(usershell).lower() + DEFAULT
        if conf == "cancel":
            return
        elif conf == 'y':
            break
        elif conf == 'c' or conf == 'n':
            continue
        else:
            print(f"{shell_err} '{conf}'is an invalid answer!{DEFAULT}")
            continue
    while True:
        conf = input(f"Will the base branch be other than 'main'? ['y' for yes, 'n' for no]\n{usershell}").lower + DEFAULT
        if conf == "cancel":
            return
        elif conf == 'y':
            base_branch = "main"
            break
        elif conf == 'n':
            while True:
                base_branch = input(f"{shell}What's the base branch?\n{usershell}") + DEFAULT
                print(f"The base branch name will be '{base_branch}'. Confirm that? ['y' for yes, 'c' or 'n' to change the name]")
                conf = input(usershell).lower() + DEFAULT
                if conf == "cancel":
                    return
                elif conf == 'y':
                    break
                elif conf == 'c' or conf == 'n':
                    continue
                else:
                    print(f"{shell_err} '{conf}'is an invalid answer!{DEFAULT}")
                    continue
        else:
            print(f"{shell_err} '{conf}'is an invalid answer!{DEFAULT}")
            continue
    mk_new_branch(path, branch_name, base_branch)


@contextmanager
# Method to prevent user from ending the exam using ctrl
def block_signals():
    o_sigint = signal.getsignal(signal.SIGINT)
    o_sigquit = signal.getsignal(signal.SIGQUIT)

    def do_noth(*args):
        pass
    signal.signal(signal.SIGINT, do_noth)
    signal.signal(signal.SIGQUIT, do_noth)
    try:
        yield
    finally:
        signal.signal(signal.SIGINT, o_sigint)
        signal.signal(signal.SIGQUIT, o_sigquit)


def handle_cd(new_path: str):
    if new_path == "cd":
        print(f"{shell_err} 'cd' needs a path")
        return
    if "cd " in new_path:
        new_path = new_path.replace("cd ", '')
    if "cd" in new_path:
        new_path = new_path.replace("cd", '')
    if "~" in new_path:
        try:
            os.chdir("~")
        except:
            print(f"{shell_err} not able to reach home!{DEFAULT}")
        return
    try:
        current = get_current_path()
        new_path = f"{current}/{new_path}"
        os.chdir(new_path)
    except:
        print(f"{shell_err} not able to reach '{new_path}'!{DEFAULT}")


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
        print(f"{shell_err} Not able to access path '{to_list}': {e}{DEFAULT}")
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
        print(f"{shell_err} ls flags are not implemented!{DEFAULT}")
    elif f_entry == "~":
        print(f"{shell_err} enter a valid path!{DEFAULT}")
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


valid_entries = BOLD + """
pull: check is pulling is necessary
commit: add and commit updates
push: push updates
branch: create a new branch
cancel: to finish any operation [cancel does not work on input mode,
        entry 'eof' to finish them]. You will be informed when you
        enter a input mode.
shells command: clear, ls [no flags], cd (or just the path), and exit
[note: commands with 'CTRL' do not work while managit shell is running!
memory {arrow up or down to access previous commands} is not active]""" + DEFAULT

def managit_shell():
    global path
    print(init_txt)
    print(f"{CYAN}           Welcome to Managit, Your personal git manager!{DEFAULT}")
    print(f"{GREEN}{valid_entries}{DEFAULT}")
    qsig = 0
    while qsig == 0:
        with block_signals():
            path = get_current_path()
            update_shellsname(path)
            entry = input(usershell).strip()
            if entry.lower() == "exit":
                qsig = 1
            elif cnt_pipes(entry):
                print(f"{shell_err} pipes are not supported yet!{DEFAULT}")
            elif entry.lower().startswith("cd ") or entry.startswith("..") or entry.lower() == "cd":
                handle_cd(entry)
            elif check_dir_exits(entry):
                handle_cd(entry)
            elif entry.lower() == "clear":
                clear()
            elif entry.lower().startswith("ls ") or entry.lower() == 'ls':
                handle_ls(entry)
            elif entry.lower() == "pull":
                handle_pull(path)
            elif entry.lower() == "commit":
                handle_commit(path)
            elif entry.lower() == "push":
                handle_push(path)
            elif entry.lower() == "branch":
                handle_new_branch(path)
            else:
                print(f"{shell_err} '{entry}' is an invalid entry, the valid entries are{DEFAULT}{valid_entries}")
