from managit.utils.colors import CYAN, GREEN, YLOW, RED, PINK, DEFAULT, BOLD
from managit.src.get_commit_info import get_commit_info
from managit.src.parser_git_status import handle_print_status, return_untracked
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
    except subprocess.CalledProcessError as e:
        print(f"{PRMT.ERR}pulling failed: {e}{DEFAULT}")
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
    except subprocess.CalledProcessError as e:
        print(f"{PRMT.ERR}checking need of pulling failed: {e}{DEFAULT}")
    except FileNotFoundError:
        print(f"{PRMT.ATT}No '.git' was found in the current path {PINK}'{path}'!{DEFAULT}")
    except OSError as e:
        print(f"{PRMT.ERR}Error on accessing the repository directory: {e}{DEFAULT}")


def handle_status(path: str):
    fpath = os.path.expanduser(path)
    try:
        ret = subprocess.run(["git", "status", "--porcelain=v2", "--branch"], cwd=fpath, check=True, text=True, capture_output=True)
        handle_print_status(ret.stdout)
        #print(ret.stdout)
    except subprocess.CalledProcessError as e:
        print(f"{PRMT.ERR}status failed: {e}{DEFAULT}")
    except FileNotFoundError:
        print(f"{PRMT.ATT}No '.git' was found in the current path {PINK}'{path}'!{DEFAULT}")
    except OSError as e:
        print(f"{PRMT.ERR}Error on accessing the repository directory: {e}{DEFAULT}")


def mk_add(path: str, files: list): #this is a mess, but i'm tired of working in add...
    fpath = os.path.expanduser(path)
    files_not_found = []
    files_found = []
    for file in files:
        try:
            ord = ["git", "add", file]
            subprocess.run(ord, cwd=fpath, check=True, capture_output=True)
            files_found.append(str(file))
        except subprocess.CalledProcessError:
            files_not_found.append(str(file))
        except FileNotFoundError:
            print(f"{PRMT.ATT}No '.git' was found in the current path {PINK}'{path}'!{DEFAULT}")
        except OSError as e:
            print(f"{PRMT.ERR}Error on accessing the repository directory: {e}{DEFAULT}")
    files_cnt = len(files_found) + len(files_not_found)
    if files_found:
        for file_found in files_found:
            if file_found == "." or file_found == "*" and files_cnt <= 1:
                print(f"{GREEN}Successfully added the changes of all files within the \"{PINK}{fpath}{GREEN}\" path into track stage!{DEFAULT}")
                break
            if '*' in file_found and file_found != '*':
                print(f"{GREEN}Successfully added the changes of all files within the \"{PINK}{file_found}{GREEN}\" pattern into track stage!{DEFAULT}")
            else:
                print(f"{GREEN}Successfully added the changes of '{PINK}{file_found}{GREEN}' into track stage!{DEFAULT}")
    if files_not_found:
        for file_not_found in files_not_found:
            if file_not_found == "." or file_not_found == "*" and files_cnt <= 1:
                print(f"{YLOW}ATTENTION: files within the \"{PINK}{fpath}{YLOW}\" path were not found!{DEFAULT}")
                return
            if '*' in file_not_found and file_not_found != '*':
                print(f"{YLOW}ATTENTION: files within the \"{PINK}{file_not_found}{YLOW}\" pattern were not found!{DEFAULT}")
            else:
                print(f"{YLOW}ATTENTION:'{PINK}{file_not_found}{YLOW}' was not found to be added!{DEFAULT}")


def _get_file_pattern_list(base_name: str):
    find_pattern_init = base_name.index("{")
    pattern_nbrs = str(base_name[find_pattern_init:]).replace("{", "").replace("}", "")
    temp = pattern_nbrs.split("..")
    init_nb = int(temp[0])
    end_nb = int(temp[-1])
    splited = list(base_name[:find_pattern_init])
    base_name = "".join(splited)
    ret = []
    if init_nb > end_nb:
        for i in range(end_nb, init_nb + 1):
            ret.append(f"{base_name}{i}")
    if end_nb > init_nb:
        for i in range(init_nb, end_nb + 1):
                ret.append(f"{base_name}{i}")
    else:
        return [f"{base_name}{init_nb}"]
    return ret


def handle_add(path: str, entry: str):
    files = []
    if entry.strip() == "add" or entry.strip() == "*":
        files = ["."]
    else:
        entry = entry.replace("add ", "")
        entry_files = entry.split()
        for file in entry_files:
            if file.endswith('}') and file[-6] == '{':
                pattened_files = _get_file_pattern_list(file)
                for pattened_file in pattened_files:
                    files.append(pattened_file)
            else:
                files.append(file)
    mk_add(path, files)


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


def check_untracked(path: str):
    fpath = os.path.expanduser(path)
    try:
        ret = subprocess.run(["git", "status", "--porcelain=v2", "--branch"], cwd=fpath, check=True, text=True, capture_output=True)
        files_track_stage = return_untracked(ret.stdout)
        untracked = 0
        for file_status in files_track_stage:
            if "untracked" in file_status or "not staged" in file_status and untracked == 0:
                print(f"{YLOW}ATTENTION: Some files are untracked (run 'add' to include them in next commit):{DEFAULT}")
                untracked = 1
            if "not staged:" in file_status:
                print(f"{RED}   [need to be add] | {file_status.replace('\n', '').strip()}{DEFAULT}")
            elif str(file_status).strip().startswith("untracked"):
                print(f"{RED}   [need to be add] | {file_status.replace('\n', '').strip()}{DEFAULT}")
        if untracked:
            answer = input(f"{CYAN}Do you want to continue to commit without adding this files?\n{DEFAULT + BOLD}['y' for yes, 'n' for no]\n-> ")
            while True:
                if answer == 'y':
                    break
                elif answer == 'n':
                    return "canceled"
                else:
                    answer = input(f"{CYAN}Please, answer 'y' for yes or 'n' for no!\n{DEFAULT + BOLD}-> ")
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        pass
    except OSError as e:
        pass
    return "continue"


def mk_commit(path: str, commit_text: str, other_text: list = []):
    fpath = os.path.expanduser(path)
    try:
        ord = ["git", "commit", "-m"]
        ord.append(commit_text)
        for i in other_text:
            if i != '':
                ord.append("-m")
                ord.append(i)
        subprocess.run(ord, cwd=fpath, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"{PRMT.ERR}commiting failed: {e}{DEFAULT}")
    except FileNotFoundError:
        print(f"{PRMT.ATT}No '.git' was found in the current path {PINK}'{path}'!{DEFAULT}")
    except OSError as e:
        print(f"{PRMT.ERR}Error on accessing the repository directory: {e}{DEFAULT}")


def handle_commit(path: str):
    cont = check_untracked(path)
    if cont == "canceled":
        return
    cmt_text, ocmt_ls = get_commit_info()
    if cmt_text == "canceled":
        return
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
        print(f"{PRMT.ERR}push failed: {e}{DEFAULT}")
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
    print(f"{PRMT.MANA}Everything was pushed!")


def mk_new_branch(path: str, branch_name: str, base_branch: str):
    fpath = os.path.expanduser(path)
    ord = ["git", "checkout", "-b", branch_name, base_branch]
    try:
        subprocess.run(ord, cwd=fpath, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"{PRMT.ERR}making a new branch failed: {e}{DEFAULT}")
    except FileNotFoundError:
        print(f"{PRMT.ATT}No '.git' was found in the current path {PINK}'{path}'!{DEFAULT}")
    except OSError as e:
        print(f"{PRMT.ERR}Error on accessing the repository directory: {e}{DEFAULT}")


def handle_new_branch(path):
    while True:
        print(f"{PRMT.MANA}What's the new branch name?{DEFAULT}")
        branch_name = input(f"{PRMT.USER}")
        if branch_name == "cancel":
            return
        print(f"The new branch name will be '{branch_name}'. Confirm that? ['y' for yes, 'n' to change the name and 'c' or 'cancel' to cancel the process]")
        conf = input(PRMT.USER).lower()
        if conf == "cancel" or conf == 'c':
            return
        elif conf == 'y':
            break
        elif conf == 'n':
            continue
        else:
            print(f"{PRMT.ERR} '{conf}'is an invalid answer!{DEFAULT}")
            continue
    while True:
        print("Will the base branch be other than 'main'? ['y' for yes, 'n' for no]" + DEFAULT)
        conf = input(f"{PRMT.USER}").lower
        if conf == "cancel":
            return
        elif conf == 'y':
            base_branch = "main"
            break
        elif conf == 'n':
            while True:
                print(f"{PRMT.MANA}What's the base branch?{DEFAULT}")
                base_branch = input(f"{PRMT.USER}")
                print(f"The base branch name will be '{base_branch}'. Confirm that? ['y' for yes, 'n' to change the base branch and 'c' or 'cancel' to cancel the process]{DEFAULT}")
                conf = input(PRMT.USER).lower()
                if conf == "cancel" or conf == 'c':
                    return
                elif conf == 'y':
                    break
                elif conf == 'n':
                    continue
                else:
                    print(f"{PRMT.ERR} '{conf}'is an invalid answer!{DEFAULT}")
                    continue
        else:
            print(f"{PRMT.ERR} '{conf}'is an invalid answer!{DEFAULT}")
            continue
    mk_new_branch(path, branch_name, base_branch)
