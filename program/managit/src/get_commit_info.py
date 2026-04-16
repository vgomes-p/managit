from managit.utils.colors import RED, CYAN, YLOW, GREEN, PINK, DEFAULT, BOLD
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

SCOPE_TXT = """╔═ What is a scope? ═══════════════════════════════════════════════╗
║ Scope is where the main changes happened                         ║
║ Example:                                                         ║
║ feat(hello_world): now the function finish with a new line       ║
╚══════════════════════════════════════════════════════════════════╝"""

ATTENTION_TXT = """╔══════════════════════════════════════════════════════════════════╗
║ Attention adds a '!' to the commit message, it will be something ║
║ like this:                                                       ║
║ wip!: now the function receives a string and print is in the...  ║
╚══════════════════════════════════════════════════════════════════╝"""

HEADER_EXAMPLE = "feat(hello_world): now the function finish with a new line"

BODY_EXAMPLE = """BREAKING CHANGE: the function now receives a string, the string
received will be printed after 'Hello, '!

Now the function finish the strin with a new line."""

FOOTER_EXAMPLE = """Reviewed-by: vgomes-p
Refs: #123"""


init_dict = {
    1: "code",
    2: "process",
    3: "doc",
}

code_dict = {
    1: "feat",
    2: "wip",
    3: "refactor",
    4: "fix",
    5: "perf",
    6: "style",
    7: "delete",
    8: "revert",
    9: "chore",
}

process_dict = {
    1: "build",
    2: "ci",
}

base_explain_dict = {
    "doc": "what kind of documentation you made!",
    "feat": "the feature(s) you implemented!",
    "wip": "the process you working at!",
    "refactor": "the improvement(s) you made!",
    "fix": "what you fixed!",
    "perf": "the performace improvement you made!",
    "style": "where you made the code clean!",
    "delete": "what you deleted and why!",
    "revert": "what went wrong!",
    "chore": "what you did...",
    "build": "the dependencies/build changes you made.",
    "ci": "the changes you made at the CI/CD.",
}

base_explain_list = ["doc", "feat", "wip", "refactor",
                     "fix", "perf", "style", "delete",
                     "revert", "chore", "build", "ci",]


def color_text(text: str, color: str, original_color: str):
    return f"║ {color}{text}{original_color}{" " * (65 - len(text))}║\n"


def box(colored_text: str, colored: str, original_color: str, reset: str):
    ret = []
    ref_text = ["feat(hello_world): now the function finish with a new line",
    "",
    "BREAKING CHANGE: the function now receives a string, the string",
    "received will be printed after 'Hello, '!",
    "",
    "Now the function finish the strin with a new line.",
    "",
    "Reviewed-by: vgomes-p",
    "Refs: #123"]
    to_color = colored_text.split('\n')
    ret.append(f"{original_color}╔{'═' * 66}╗\n")
    for i in ref_text:
        if i in to_color:
            to_color.remove(i)
            ret.append(color_text(i, colored, original_color))
        else:
            ret.append(color_text(i, original_color, original_color))
    ret.append(f"╚{'═' * 66}╝{reset}")
    return "".join(ret)


def _error(pos: str):
    clear()
    print(f"{RED}Serious error in {pos}{DEFAULT}")
    exit


def get_commit_body():
    print(f"{CYAN}Note: 'cancel' does not work in the input mode, entry 'eof' and 'EOF' finish input mode.")
    add = 'y'
    more_detail = []
    while add == 'y':
        print(f"{CYAN}┌[INPUT MODE, 'eof' and 'EOF' finish]{'─' * (66 - 36)}┐")
        print(f"│ Write what you want to add, this is the time to explain things!{' ' * (66 - 64)}│")
        detail_to_add = []
        first_ln = 0
        while True:
            to_add = input("├ ").strip()
            if to_add.lower() == "eof":
                break
            if first_ln == 0:
                first_ln = 1
            else:
                detail_to_add.append('\n')
            detail_to_add.append(to_add)
        print(f"└{'─' * 66}┘{DEFAULT}")
        detail_added = "".join(detail_to_add)
        more_detail.append(detail_added)
        print(f"{CYAN}┌{'─' * 66}┐")
        print(f"│ Do you want to one more body? Note: this will not be the footer!{' ' * (66 - 65)}│")
        print(f"└['y' for yes and 'n' for no, and 'c' to cancel the commit]{'─' * (66 - 58)}┘{DEFAULT}")
        check = input(f"{BOLD}-> ").lower()
        while True:
            if check == "cancel":
                return ["cancelled", ]
            elif check == 'y':
                break
            elif check == 'n':
                add = check
                break
            else:
                check = input(f"{RED}Invalid entry, please choose 'y' or 'n': {DEFAULT}{BOLD}")
                continue
    return more_detail


def _add_footer_detail():
    print(f"{CYAN}Note: 'cancel' does not work in the input mode, entry 'eof' and 'EOF' finish input mode.")
    print(f"{CYAN}┌[INPUT MODE, 'eof' and 'EOF' finish]{'─' * (66 - 36)}┐")
    print(f"│ Write what you want to add{' ' * (66 - 27)}│")
    detail_to_add = []
    while True:
        to_add = input("├ ").strip()
        if to_add.lower() == "eof":
            break
        detail_to_add.append('\n')
        detail_to_add.append(to_add)
    print(f"└{'─' * 66}┘{DEFAULT}")
    return "".join(detail_to_add)


def get_commit_footer():
    reviewer = input(f"{CYAN}Reviewed-by: {DEFAULT}{BOLD}")
    refs = input(f"{CYAN}Refs: {DEFAULT}{BOLD}")
    commit_footer = ["Reviewed-by: ", reviewer, "\nRefs: ", refs,]
    print(f"{CYAN}┌{'─' * 66}┐")
    print(f"│ Add more detail to the footer?{' ' * (66 - 31)}│")
    print(f"└['y' for yes and 'n' for no, and 'c' to cancel the commit]{'─' * (66 - 58)}┘{DEFAULT}")
    check = input(f"{BOLD}-> ").lower()
    while True:
        if check == "cancel":
            return ["cancelled", ]
        elif check == 'y':
            more_detail = _add_footer_detail()
            commit_footer.append(more_detail)
            break
        elif check == 'n':
            break
        else:
            check = input(f"{RED}Invalid entry, please choose 'y' or 'n': {DEFAULT}{BOLD}")
            continue
    return "".join(commit_footer)


def pick_type():
    pick_type = input(f"{CYAN}{INIT_TXT}{DEFAULT}{BOLD}\n-> ").strip()
    while True:
        valid_entry = ["1", "2", "3"]
        if pick_type == "cancel":
            return "canceled"
        elif is_valid_number(pick_type) and str(pick_type) in valid_entry:
            break
        else:
            pick_type = input(f"{RED}Invalid entry, please choose 1, 2 or 3: {DEFAULT}{BOLD}")
            continue
    return str(init_dict[int(pick_type)])


def pick_tag(type_picked: str):
    if type_picked == "code":
        pick_tag = input(f"{CYAN}{CODE_TXT}{DEFAULT}\n{BOLD}-> ")
        while True:
            valid_entry = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
            if pick_tag == "cancel":
                return "canceled"
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
                return "canceled"
            elif is_valid_number(pick_tag) and str(pick_tag) in valid_entry:
                break
            else:
                pick_tag = input(f"{RED}Invalid entry, please choose 1 or 2: {DEFAULT}{BOLD}")
                continue
        tag_picked = process_dict[int(pick_tag)]
    elif type_picked == "doc":
        tag_picked = type_picked
    else:
        return "error"
    return str(tag_picked)


def get_explain_txt(tag_picked: str):
    if tag_picked in base_explain_list:
        return str(base_explain_dict[str(tag_picked)])
    else:
        return "error"


def get_scope():
    clear()
    print(f"{YLOW}{SCOPE_TXT}{DEFAULT}")
    print(f"{CYAN}┌{'─' * 66}┐")
    print(f"│ Do you want to add a commit scope?{' ' * (66 - 35)}│")
    print(f"└['y' for yes and 'n' for no, and 'c' to cancel the commit]{'─' * (66 - 58)}┘{DEFAULT}")
    answer = input(f"{BOLD}-> ").lower()
    while True:
        if answer == "c":
            return "canceled"
        elif answer == 'y':
            scope = input(f"{CYAN}What is the scope for this commit?{DEFAULT}\n{BOLD}-> ")
            check_scope = input(f"{CYAN}The scope will be '{scope}', are you sure? ['y' for yes and 'n' for no, and 'c' to cancel commit]{DEFAULT}\n{BOLD}->")
            while True:
                if check_scope.lower() == 'c':
                    return 'canceled'
                elif check_scope.lower() == 'y':
                    return f"({scope})"
                elif check_scope.lower() == 'n':
                    scope = input(f"{CYAN}What is the scope for this commit?{DEFAULT}\n{BOLD}-> ")
                    continue
                else:
                    print(f"{RED}Invalid entry, please choose 'y', 'n' or 'c'!{DEFAULT}")
                    continue
        elif answer == 'n':
            return ""
        else:
            answer = input(f"{RED}Invalid entry, please choose 'y', 'n' or 'c': {DEFAULT}{BOLD}")
            continue


def needs_attention():
    clear()
    print(f"{YLOW}{ATTENTION_TXT}{DEFAULT}")
    print(f"{CYAN}┌{'─' * 66}┐")
    print(f"│ Do this commit needs attention?{' ' * (66 - 32)}│")
    print(f"└['y' for yes and 'n' for no, and 'c' to cancel the commit]{'─' * (66 - 58)}┘{DEFAULT}")
    answer = input(f"{BOLD}-> ").lower()
    while True:
        if answer == "c":
            return "canceled"
        elif answer == 'y':
            return "!"
        elif answer == 'n':
            return ""
        else:
            answer = input(f"{RED}Invalid entry, please choose 'y', 'n' or 'c': {DEFAULT}{BOLD}")
            continue


def get_commit_header(explain_txt: str, tag_picked: str):
    clear()
    print(f"{YLOW}This is a sum up and you have a single line keep is short!{CYAN}")
    print(f"┌[SINGLE LINE INPUT MODE]{'─' * (66 - 24)}┐")
    print(f"│ Tell me more about {explain_txt}{" " * ((66 - 20) - len(explain_txt))}│")
    while True:
        to_add = input("├ ").strip()
        if to_add == '':
            print(f"├ {RED}Ops... header cannot be empty! Write something!{'' * 16}|{CYAN}")
            continue
        else:
            commit_summary = to_add
            break
    print(f"└{'─' * 66}┘{DEFAULT}")
    scope = get_scope()
    if scope == "canceled":
        return "canceled"
    attention = needs_attention()
    if attention == "canceled":
        return "canceled"
    return f"{tag_picked}{scope}{attention}: {commit_summary}"


def add_commit_message(message_type: str):
    print(f"{CYAN}┌{'─' * 66}┐")
    print(f"│ Do you want to add a commit {message_type}{" " * (37 - len(message_type))}│")
    print(f"└['y' for yes and 'n' for no, and 'c' to cancel the commit]{'─' * (66 - 58)}┘{DEFAULT}")
    answer = input(f"{BOLD}-> ").lower()
    while True:
        if answer == "c":
            return "canceled"
        elif answer == 'y':
            return "y"
        elif answer == 'n':
            return "n"
        else:
            answer = input(f"{RED}Invalid entry, please choose 'y','n' or 'c': {DEFAULT}{BOLD}")
            continue


def get_commit_info():
    commit_detail = []
    clear()
    print(f"{CYAN}Example of a commit (header colored).{DEFAULT}")
    print(box(HEADER_EXAMPLE, PINK, GREEN, CYAN))
    print(f"All information you give will be used to build the commit's header.{DEFAULT}")
    type_picked = pick_type()
    if type_picked == "canceled":
        return type_picked, []
    tag_picked = pick_tag(type_picked)
    if tag_picked == "canceled":
        return tag_picked, []
    if tag_picked == "error":
        _error("get_commit_info(): failed to pick tag")
        return "error", []
    explain_txt = get_explain_txt(tag_picked)
    if explain_txt == "error":
        _error("get_commit_info(): failed to pick explanation text")
        return "error", []
    commit_header = get_commit_header(explain_txt, tag_picked)
    if commit_header == "canceled":
        return "canceled", []
    clear()
    print(f"{CYAN}Now you will be able to add a body to the commit. Here an example (colored text):")
    print(box(BODY_EXAMPLE, PINK, GREEN, DEFAULT))
    add_body = add_commit_message("body? Time to give more details...")
    if add_body == "canceled":
        return "canceled", []
    elif add_body == 'y':
        commit_detail = get_commit_body()
    else:
        pass
    clear()
    print(f"{CYAN}Now you will be able to add a footer to the commit. Here an example (colored text):")
    print(box(FOOTER_EXAMPLE, PINK, GREEN, DEFAULT))
    add_footer = add_commit_message("footer?")
    if add_footer == "canceled":
        return "canceled", []
    elif add_footer == 'y':
        commit_footer = str(get_commit_footer())
        commit_detail.append(commit_footer)
    else:
        pass
    return commit_header, commit_detail
