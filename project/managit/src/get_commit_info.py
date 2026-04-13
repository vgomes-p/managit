from managit.utils.colors import RED, CYAN, DEFAULT, BOLD
from managit.utils.nbr import is_valid_number
from managit.utils.clear import clear

INIT_TXT = """┌─ What type of commit is ─────────────────────────────────────────┐
│ 1: Code related commit                                           │
│ 2: Process related commit                                        │
│ 3: Documentation                                                 │
└──────────────────────────────────────────────────────────────────┘"""

CODE_TXT = """┌─ What is the main type of change you've made for this commit? ───┐
│ 1: Added new feature                                             │
│ 2: Working in progress                                           │
│ 3: Improved a function                                           │
│ 4: Fixed a bug or error                                          │
│ 5: Improved the code performance                                 │
│ 6: Formatted the code - made it clean                            │
│ 7: Deleted something that was not being used                     │
│ 8: Returning to the previous version due to a error              │
│ 9: Made changed that didn't affected the code directly           │
└──────────────────────────────────────────────────────────────────┘"""

PROCESS_TXT = """┌─ What is the main type of change you've made for this commit? ───┐
│ 1: Changes related to build and extern dependencies system       │
│ 2: Changes related to continued-integration (CI/CD) process      │
└──────────────────────────────────────────────────────────────────┘"""

init_dict = {
    1: "code",
    2: "process",
    3: "doc:",
}

code_dict = {
    1: "feat:",
    2: "wip:",
    3: "refactor:",
    4: "fix:",
    5: "perf:",
    6: "style:",
    7: "delete:",
    8: "revert:",
    9: "chore:",
}

process_dict = {
    1: "build:",
    2: "ci:",
}

base_explain_dict = {
    "doc:": "what kind of documentation you made!",
    "feat:": "the feature(s) you implemented!",
    "wip:": "the process you working at!",
    "refactor:": "the improvement(s) you made!",
    "fix:": "what you fixed!",
    "perf:": "the performace improvement you made!",
    "style:": "where you made the code clean!",
    "delete:": "what you deleted and why!",
    "revert:": "what went wrong!",
    "chore:": "what you did...",
    "build:": "the dependencies/build changes you made.",
    "ci:": "the changes you made at the CI/CD.",
}

base_explain_list = ["doc:", "feat:", "wip:", "refactor:",
                     "fix:", "perf:", "style:", "delete:",
                     "revert:", "chore:", "build:", "ci:",]


def _error(pos: str):
    clear()
    print(f"{RED}Serious error in {pos}{DEFAULT}")
    exit


def _add_more_detail():
    print(f"{CYAN}Note, each detail will be added as a message (-m '<what you adding>')!\n",
          "Note: 'cancel' does not work in the input mode, entry 'eof' and 'EOF' finish input mode.")
    add = 'y'
    more_detail = []
    while add == 'y':
        print(f"{CYAN}┌[INPUT MODE, 'eof' and 'EOF' finish]──────────────────────────────┐")
        print("│ Write what you want to add, this is the time to explain things!  │")
        detail_to_add = []
        while True:
            to_add = input("├ ").strip()
            if to_add.lower() == "eof":
                break
            detail_to_add.append(to_add)
            detail_to_add.append('\n')
        print(f"└──────────────────────────────────────────────────────────────────┘\n{DEFAULT}")
        detail_added = "".join(detail_to_add)
        more_detail.append(detail_added)
        print(f"{CYAN}┌──────────────────────────────────────────────────────────────────┐")
        print(f"│ Do you want to add more details? Time to give more details...    │")
        print(f"└['y' for yes and 'n' for no]──────────────────────────────────────┘{DEFAULT}")
        check = input(f"{BOLD}-> ").lower()
        while True:
            if check == "cancel":
                return []
            elif check == 'y':
                break
            elif check == 'n':
                add = check
                break
            else:
                check = input(f"{RED}Invalid entry, please choose 'y' or 'n': {DEFAULT}{BOLD}")
                continue
    return more_detail


def get_commit_info():
    pick_type = input(f"{CYAN}{INIT_TXT}{DEFAULT}{BOLD}\n-> ").strip()
    while True:
        valid_entry = ["1", "2", "3"]
        if pick_type == "cancel":
            return "canceled", []
        elif is_valid_number(pick_type) and str(pick_type) in valid_entry:
            break
        else:
            pick_type = input(f"{RED}Invalid entry, please choose 1, 2 or 3: {DEFAULT}{BOLD}")
            continue

    type_picked = str(init_dict[int(pick_type)])
    if type_picked == "code":
        pick_tag = input(f"{CYAN}{CODE_TXT}{DEFAULT}\n{BOLD}-> ")
        while True:
            valid_entry = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
            if pick_tag == "cancel":
                return "canceled", []
            elif is_valid_number(pick_tag) and str(pick_tag) in valid_entry:
                break
            else:
                pick_tag = input(f"{RED}Invalid entry, please choose a number between 1 and 9: {DEFAULT}{BOLD}")
                continue
        tag_picked = code_dict[int(pick_tag)]

    elif type_picked == "process":
        pick_tag = input(f"{CYAN}{PROCESS_TXT}{DEFAULT}\n{BOLD}-> ")
        while True:
            valid_entry = ["1", "2"]
            if pick_tag == "cancel":
                return "canceled", []
            elif is_valid_number(pick_tag) and str(pick_tag) in valid_entry:
                break
            else:
                pick_tag = input(f"{RED}Invalid entry, please choose 1 or 2: {DEFAULT}{BOLD}")
                continue
        tag_picked = process_dict[int(pick_tag)]

    elif type_picked == "doc:":
        tag_picked = "doc:"

    else:
        _error("get_commit_info(): failed to pick tag")

    if tag_picked in base_explain_list:
        explain_txt = base_explain_dict[str(tag_picked)]
    else:
        _error("get_commit_info(): failed to pick explanation text")

    print(f"{CYAN}Note: 'cancel' does not work in this input mode, entry 'eof' and 'EOF' finish input mode.\nThis is a sum up, not the whole explanation, keep is short!")
    print(f"{CYAN}┌[INPUT MODE, 'eof' and 'EOF' finish]──────────────────────────────┐")
    print(f"│ Tell me more about {explain_txt}", " " * (44 - len(explain_txt)), "│")
    cmt_explain = []
    while True:
        to_add = input("├ ").strip()
        if to_add.lower() == "eof":
            break
        cmt_explain.append(to_add)
        cmt_explain.append('\n')
    print(f"└──────────────────────────────────────────────────────────────────┘\n{DEFAULT}")
    commit_body = "".join(cmt_explain)
    main_commit = f"{tag_picked} {commit_body}"

    print(f"{CYAN}┌──────────────────────────────────────────────────────────────────┐")
    print(f"│ Do you want to add more details? Time to give more details...    │")
    print(f"└['y' for yes and 'n' for no]──────────────────────────────────────┘{DEFAULT}")
    yon = input(f"{BOLD}-> ").lower()
    more_detail = []
    while True:
        if yon == "cancel":
            return "canceled", []
        elif yon == 'y':
            more_detail = _add_more_detail()
            break
        elif yon == 'n':
            break
        else:
            yon = input(f"{RED}Invalid entry, please choose 'y' or 'n': {DEFAULT}{BOLD}")
            continue

    return main_commit, more_detail
