from managit.utils.colors import CYAN, YLOW, RED, BOLD, DEFAULT
import os


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


MANA, ATT, ERR, USER = "", "", "", ""


def update_shells_prompt(path: str):
    global MANA, ATT, ERR, USER
    username = get_user()
    paths = get_pathsumup(path)
    MANA = f"{CYAN}{paths} | managit $ {DEFAULT}{BOLD}"
    ATT = f"{CYAN}{paths} | managit ${YLOW} ATTENTION:"
    ERR = f"{CYAN}{paths} | managit ${RED} ERROR:"
    USER = f"{CYAN}{paths} | {username} $ {DEFAULT}{BOLD}"
