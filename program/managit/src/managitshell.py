from managit.utils.clear import clear
from managit.utils.colors import CYAN, DEFAULT, GREEN, BOLD
from managit.src.shells_prompt import update_shells_prompt
import managit.src.shells_prompt as PRMT
from managit.src.git_cmds import handle_commit, handle_new_branch, handle_pull, handle_push, handle_status, handle_add
from managit.src.shell_cmds import handle_cd, handle_ls, cnt_pipes, check_dir_exits, get_current_path
from contextlib import contextmanager
import signal

init_txt = CYAN + """┌──────────────────────────────────────────────────────────────────┐
│╔════════════════════════════════════════════════════════════════╗│
│║ ██      ██  ██████  ██   ██  ██████  ███████  ██████  ████████ ║│
│║ ██████████  ██  ██  ███  ██  ██  ██  ██         ██       ██    ║│
│║ ██  ██  ██  ██████  ██ █ ██  ██████  ██ ████    ██       ██    ║│
│║ ██      ██  ██  ██  ██  ███  ██  ██  ██   ██    ██       ██    ║│
│║ ██      ██  ██  ██  ██   ██  ██  ██  ███████  ██████     ██    ║│
│╚════════════════════════════════════════════════════════════════╝│
└──────────────────────────────────────────────────────────────────┘""" + DEFAULT


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


valid_entries = BOLD + """
pull:   check if pulling is necessary
status: shows the track of files in the repository.
commit: add and commit updates
push:   push updates
branch: create a new branch
cancel: to finish any operation [cancel does not work on input mode,
        entry 'eof' to finish them]. You will be informed when you
        enter a input mode.
shells command: clear, ls [no flags], cd (or just the path), and exit
[note: commands with 'CTRL' do not work while managit shell is running!
memory {arrow up or down to access previous commands} is not active]""" + DEFAULT


others_cmds = {"pull": handle_pull,
        "status": handle_status,
        "commit": handle_commit,
        "push": handle_push,
        "branch": handle_new_branch,
}

special_cmds = ["clear", "ls", "cd", "add"]

def exec_others_cmd(cmd: str, path: str):
    exec = others_cmds.get(cmd)
    if exec:
        exec(path)
    else:
        print(f"{PRMT.ERR} '{cmd}' is an invalid entry, the valid entries are{DEFAULT}{valid_entries}")


def exec_special_cmds(entry: str, path: str):
    if cnt_pipes(entry):
        print(f"{PRMT.ERR} pipes are not supported yet!{DEFAULT}")
    elif entry.lower() == "clear":
        clear()
    elif (entry.lower().startswith("cd ") or
        entry.startswith("..") or
        entry.lower() == "cd" or
        check_dir_exits(entry)):
        handle_cd(entry)
    elif entry.lower().startswith("add"):
        handle_add(path, entry)
    elif entry.lower().startswith("ls ") or entry.lower() == 'ls':
        handle_ls(entry)


def managit_shell():
    print(init_txt)
    print(f"{CYAN}           Welcome to Managit, Your personal git manager!{DEFAULT}")
    print(f"{GREEN}{valid_entries}{DEFAULT}")
    qsig = 0
    while qsig == 0:
        with block_signals():
            path = get_current_path()
            update_shells_prompt(path)
            entry = input(PRMT.USER).strip()
            parser_entry = entry.split()
            if entry.lower() == "exit":
                qsig = 1
            elif (parser_entry[0] in special_cmds or
                  entry.startswith("..") or
                  check_dir_exits(entry)):
                exec_special_cmds(entry, path)
            else:
                exec_others_cmd(parser_entry[0], path)
