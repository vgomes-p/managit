from managit.utils.clear import clear
from managit.utils.colors import CYAN, DEFAULT, RED, YLOW, PINK, GREEN
from managit.src.get_commit_info import get_commit_info
from contextlib import contextmanager
from time import sleep
import subprocess
import signal
import os

init_txt = """┌──────────────────────────────────────────────────────────────────┐
│╔════════════════════════════════════════════════════════════════╗│
│║ ██      ██  ██████  ██   ██  ██████  ███████  ██████  ████████ ║│
│║ ██████████  ██  ██  ███  ██  ██  ██  ██         ██       ██    ║│
│║ ██  ██  ██  ██████  ██ █ ██  ██████  ██ ████    ██       ██    ║│
│║ ██      ██  ██  ██  ██  ███  ██  ██  ██   ██    ██       ██    ║│
│║ ██      ██  ██  ██  ██   ██  ██  ██  ███████  ██████     ██    ║│
│╚════════════════════════════════════════════════════════════════╝│
│                   made by github.com/vgomes-p                    │
└──────────────────────────────────────────────────────────────────┘"""

colored_init_txt = CYAN + init_txt + DEFAULT
shell = f"{CYAN}managit $> {DEFAULT}"
shell_att = f"{YLOW}managit $> ATTENTION:"
shell_err = f"{RED}managit $> ERROR:"
user = f"{CYAN}user$> {DEFAULT}"


def get_current_path():
    return os.getcwd()


def get_pull(path: str):
    fpath = os.path.expanduser(path)
    try:
        subprocess.run(["git", "pull"], cwd=fpath, check=True, capture_output=True)
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
        ret = subprocess.run(["git", "rev-list", "--count", "HEAD..origin/HEAD"], cwd=fpath, check=True, capture_output=True)
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
        subprocess.run(["git", "add", "."], cwd=fpath, check=True, capture_output=True)
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
    print(f"{shell}Adding files from {path} to commit...")
    sleep(.3)
    mk_add(path)
    print(f"{shell}Starting the commit informations system")
    sleep(.5)
    cmt_text, ocmt_ls = get_commit_info()
    print(f"{shell}Creating commit text...")
    sleep(.4)
    print(f"{shell}Commiting to git repository...")
    mk_commit(path, cmt_text, ocmt_ls)


def mk_push(path: str, force: bool = False):
    try:
        if force:
            subprocess.run(["git", "push", "--force"], check=True, capture_output=True)
        else:
            subprocess.run(["git", "push"], check=True, capture_output=True)
    except FileNotFoundError:
        print(f"{YLOW}No .git was found in the current path {PINK}'{path}'!{DEFAULT}")


def handle_push(path):
    print(f"{shell}Do you want to force push? ['y' for yes, 'n' for no]")
    while True:
        check = input(user).lower()
        if check == 'y':
            mk_push(path, force=True)
            break
        elif check == 'n':
            mk_push(path, force=False)
            break
        else:
            print(f"{shell}please, answer 'y' for yes or 'n' for no!")
            continue
    print(f"{shell}everything was pushed!")



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


valid_entries = """
clear: clear screen
pull: check is pulling is necessary
commit: add and commit updates
push: push updates
exit: exits the program
[note: commands with 'CTRL' do not work while managit is running!]"""

def managit_shell(path: str = ""):
    print(colored_init_txt)
    print(f"{CYAN}           Welcome to Managit, Your personal git manager!{DEFAULT}")
    print(f"{GREEN}{valid_entries}{DEFAULT}")
    qsig = 0
    while qsig == 0:
        with block_signals():
            entry = input(user).strip().lower()
            path = get_current_path()
            if entry == "exit":
                qsig = 1
            elif entry == "clear":
                clear()
            elif entry == "pull":
                handle_pull(path)
            elif entry == "commit":
                handle_commit(path)
            elif entry == "push":
                handle_push(path)
            else:
                print(f"{shell}invalid entry, the valid entries are\n{valid_entries}")
