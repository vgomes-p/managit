from managit.utils.clear import clear
from managit.utils.colors import CYAN, DEFAULT, GREEN, BOLD
from managit.src.shells_prompt import update_shells_prompt
import managit.src.shells_prompt as PRMT
from managit.src.git_cmds import handle_commit, handle_new_branch, handle_pull, handle_push
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
│                   made by github.com/vgomes-p                    │
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
    print(init_txt)
    print(f"{CYAN}           Welcome to Managit, Your personal git manager!{DEFAULT}")
    print(f"{GREEN}{valid_entries}{DEFAULT}")
    qsig = 0
    while qsig == 0:
        with block_signals():
            path = get_current_path()
            update_shells_prompt(path)
            entry = input(PRMT.USER).strip()
            if entry.lower() == "exit":
                qsig = 1
            elif cnt_pipes(entry):
                print(f"{PRMT.ERR} pipes are not supported yet!{DEFAULT}")
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
                print(f"{PRMT.ERR} '{entry}' is an invalid entry, the valid entries are{DEFAULT}{valid_entries}")
