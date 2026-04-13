from managit.utils.colors import PINK, DEFAULT
from managit.src.get_commit_info import get_commit_info
import managit.src.shells_prompt as PRMT
from time import sleep
import subprocess
import os


def get_pull(path: str):
    fpath = os.path.expanduser(path)
    try:
        ord = ["git", "pull"]
        subprocess.run(ord, cwd=fpath, check=True, capture_output=True)
        print(f"{PRMT.MANA}Updates pulled!")
    except FileNotFoundError:
        print(f"{PRMT.ATT}No .git was found in the current path {PINK}'{path}'!{DEFAULT}")
    except OSError as e:
        print(f"{PRMT.ERR}Error on accessing the repository directory: {e}{DEFAULT}")


def handle_pull(path: str):
    fpath = os.path.expanduser(path)
    print(f"{PRMT.MANA}Checking if pulling is necessary...")
    sleep(.5)
    try:
        ord = ["git", "rev-list", "--count", "HEAD..origin/HEAD"]
        ret = subprocess.run(ord, cwd=fpath, check=True, capture_output=True)
        behind = int(ret.stdout.strip())
        if behind > 0:
            print(f"{PRMT.MANA}Pulling is needed. Starting pulling...")
            sleep(.5)
            print(get_pull())
        else:
            print(f"{PRMT.MANA}Nothing to pull!")
    except FileNotFoundError:
        print(f"{PRMT.ATT}No '.git' was found in the current path {PINK}'{path}'!{DEFAULT}")
    except OSError as e:
        print(f"{PRMT.ERR}Error on accessing the repository directory: {e}{DEFAULT}")


def handle_status(path: str):
    fpath = os.path.expanduser(path)

    try:
        ret = subprocess.run(["git", "status"], cwd=fpath, check=True, text=True, capture_output=True)
        print(ret.stdout, end="")
    except FileNotFoundError:
        print(f"{PRMT.ATT}No '.git' was found in the current path {PINK}'{path}'!{DEFAULT}")
    except OSError as e:
        print(f"{PRMT.ERR}Error on accessing the repository directory: {e}{DEFAULT}")


def mk_add(path: str):
    fpath = os.path.expanduser(path)
    try:
        ord = ["git", "add", "."]
        subprocess.run(ord, cwd=fpath, check=True, capture_output=True)
    except FileNotFoundError:
        print(f"{PRMT.ATT}No '.git' was found in the current path {PINK}'{path}'!{DEFAULT}")
    except OSError as e:
        print(f"{PRMT.ERR}Error on accessing the repository directory: {e}{DEFAULT}")


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
        print(f"{PRMT.ATT}No '.git' was found in the current path {PINK}'{path}'!{DEFAULT}")
    except OSError as e:
        print(f"{PRMT.ERR}Error on accessing the repository directory: {e}{DEFAULT}")


def handle_commit(path: str):
    cmt_text, ocmt_ls = get_commit_info()
    if cmt_text == "canceled":
        return
    print(f"{PRMT.MANA}Adding files from {path} to commit...")
    sleep(.3)
    mk_add(path)
    print(f"{PRMT.MANA}Starting the commit informations system")
    sleep(.5)
    print(f"{PRMT.MANA}Creating commit text...")
    sleep(.4)
    print(f"{PRMT.MANA}Commiting to git repository...")
    mk_commit(path, cmt_text, ocmt_ls)


def mk_push(path: str, force: bool = False):
    fpath = os.path.expanduser(path)
    try:
        if force:
            ord = ["git", "push", "--force"]
        else:
            ord = ["git", "push"]
        subprocess.run(ord, cwd=fpath, check=True, capture_output=True, text=True)
    except FileNotFoundError:
        print(f"{PRMT.ATT}No '.git' was found in the current path {PINK}'{path}'!{DEFAULT}")
    except subprocess.CalledProcessError as e:
        print(f"{PRMT.ERR} push failed: {e}{DEFAULT}")
    except OSError as e:
        print(f"{PRMT.ERR} {e}{DEFAULT}")


def handle_push(path):
    print(f"{PRMT.MANA}Do you want to force push? ['y' for yes, 'n' for no]")
    while True:
        check = input(PRMT.USER).lower()
        if check == "cancel":
            return
        elif check == 'y':
            mk_push(path, force=True)
            break
        elif check == 'n':
            mk_push(path, force=False)
            break
        else:
            print(f"{PRMT.MANA}please, answer 'y' for yes or 'n' for no!")
            continue
    print(f"{PRMT.MANA}everything was pushed!")


def mk_new_branch(path: str, branch_name: str, base_branch: str):
    fpath = os.path.expanduser(path)
    ord = ["git", "checkout", "-b", branch_name, base_branch]
    try:
        subprocess.run(ord, cwd=fpath, check=True, capture_output=True)
    except FileNotFoundError:
        print(f"{PRMT.ATT}No '.git' was found in the current path {PINK}'{path}'!{DEFAULT}")
    except OSError as e:
        print(f"{PRMT.ERR}Error on accessing the repository directory: {e}{DEFAULT}")


def handle_new_branch(path):
    while True:
        branch_name = input(f"{PRMT.MANA}What's the new branch name?\n{PRMT.USER}") + DEFAULT
        print(f"The new branch name will be '{branch_name}'. Confirm that? ['y' for yes, 'c' or 'n' to change the name]")
        conf = input(PRMT.USER).lower() + DEFAULT
        if conf == "cancel":
            return
        elif conf == 'y':
            break
        elif conf == 'c' or conf == 'n':
            continue
        else:
            print(f"{PRMT.ERR} '{conf}'is an invalid answer!{DEFAULT}")
            continue
    while True:
        conf = input(f"Will the base branch be other than 'main'? ['y' for yes, 'n' for no]\n{PRMT.USER}").lower + DEFAULT
        if conf == "cancel":
            return
        elif conf == 'y':
            base_branch = "main"
            break
        elif conf == 'n':
            while True:
                base_branch = input(f"{PRMT.MANA}What's the base branch?\n{PRMT.USER}") + DEFAULT
                print(f"The base branch name will be '{base_branch}'. Confirm that? ['y' for yes, 'c' or 'n' to change the name]")
                conf = input(PRMT.USER).lower() + DEFAULT
                if conf == "cancel":
                    return
                elif conf == 'y':
                    break
                elif conf == 'c' or conf == 'n':
                    continue
                else:
                    print(f"{PRMT.ERR} '{conf}'is an invalid answer!{DEFAULT}")
                    continue
        else:
            print(f"{PRMT.ERR} '{conf}'is an invalid answer!{DEFAULT}")
            continue
    mk_new_branch(path, branch_name, base_branch)
