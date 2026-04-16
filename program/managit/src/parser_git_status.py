from managit.utils.colors import CYAN, RED, GREEN, YLOW, PINK, DEFAULT, BOLD

conflits_explain = {
"UU": "[CONFLIT] Both, local and remote repository modified: ",
"AA": "[CONFLIT] Both, local and remote repository added:",
"DD": "[CONFLIT] Both, local and remote repository deleted:",
"AU": "[CONFLIT] Adds needed to be push in",
"UA": "[CONFLIT] Adds needed to be pull in ",
"UD": "[CONFLIT] Deletes needed to be push in ",
"DU": "[CONFLIT] Deletes needed to be pull in "
}

track_explain = {
".M": "modified: ",
"M.": "modified: ",
"MM": "modified: ",
"A.": "added: ",
".A": "added: ",
"D.": "deleted: ",
".D": "deleted: ",
"DD": "deleted: ",
"R.": "renamed: ",
".R": "renamed: ",
"C.": "copied: ",
".C": "copied: ",
"T.": "type changed: ",
".T": "type changed: ",
"?": "untracked file: ",
"!": "ignored: "
}

conflits_type = ["UU", "AA", "DD", "AU", "UA", "UD", "DU"]

tracks = [".M", "M.", "MM", "A.", ".A", "D.", ".D", "DD",
          "R.", ".R", "C.", ".C", "T.", ".T", "?", "!"]


def tokenizer(line: str, sep: str=" "):
    return line.split(sep)


def get_branch_stage(tokens: list):
    for i in tokens:
        if "branch.ab" in i:
            line = i
            break
        else:
            pass
    line = line.replace("# branch.ab ", "")
    tokens = tokenizer(line)
    n1 = int(tokens[0])
    n2 = int(tokens[1])
    if n1 == 0 and n2 == 0:
        ret = "Local repository is up to date."
    elif n1 != 0 and n2 == 0:
        ret = "Local repository is ahead."
    elif n1 == 0 and n2 != 0:
        ret = "Local repository is behind."
    elif n1 != 0 and n2 != 0:
        ret = "Local repository is has conflits with remote repository."
    return ret


def check_conflits(tokens: list):
    for i in tokens:
        token = tokenizer(i)
        for type in conflits_type:
            if type in token:
                return True
    return False


def get_conflits(tokens: list):
    ret = []
    for i in tokens:
        token = tokenizer(i)
        for type in conflits_type:
            if type in token:
                conflit_text = conflits_explain[type]
                file = token[-1]
                ret.append(f"{conflit_text}{file}")
    return ret


def is_files_track(line: str):
    for i in tracks:
        for j in line.split():
            if i == j:
                return True
    return False


def file_and_stage_tranlater(track: str, file: str):
    track_text = track_explain[track]
    return f"   {track_text}{file}\n"


def get_file_and_stage(line: str):
    tokens = tokenizer(line)
    if "?" in tokens:
        return tokens[0], tokens[-1]
    if "!" in tokens:
        return tokens[0], tokens[-1]
    return tokens[1], tokens[-1]


def handle_files_status(tokens: list):
    ret = []
    for i in range(0, 4):
        tokens.pop(0)
    for line in tokens:
        if is_files_track(line):
            stage, file = get_file_and_stage(line)
            if stage in tracks:
                ret.append(file_and_stage_tranlater(stage, file))
            else:
                pass
        else:
            continue
    return ret


def get_status_parts(git_return: str):
    parser = tokenizer(git_return, "\n")
    has_conflit = 0
    branch_stage = get_branch_stage(parser)
    conflits = []
    if check_conflits(parser):
        conflits = get_conflits(parser)
        has_conflit = 1
    files_track_stage = handle_files_status(parser)
    return branch_stage, conflits, files_track_stage, has_conflit

def build_new_status(branch_stage: str, conflits: list, files_track_stage: list, has_conflit: bool):
    ret = [f"{CYAN}{branch_stage}"]
    if has_conflit:
        conflit_war = f"\n{YLOW}ATTENTION: Local repository have conflits with remote repository.\nHere they are:\n"
        ret.append(conflit_war)
        for conflit in conflits:
            to_add = f" {conflit}\n" 
            ret.append(to_add)
    ret.append(f"{DEFAULT}\n")
    untracked = 0
    if files_track_stage:
        to_add = f"{CYAN}Here are the uncommited changes (run 'commit' to include them in next push):{DEFAULT}\n"
        ret.append(to_add)
        for file_status in files_track_stage:
            if "untracked" in file_status and untracked == 0:
                to_add = f"{CYAN}Untracked files (run 'commit' to include them in next push):{DEFAULT}\n"
                ret.append(to_add)
                untracked = 1
            if "modified" in file_status:
                line_color = YLOW
            elif "added" in file_status:
                line_color = GREEN
            elif "untracked" in file_status:
                line_color = PINK
            elif "ignored" in file_status:
                line_color = PINK
            elif "deleted" in file_status:
                line_color = RED
            elif "copied" in file_status:
                line_color = DEFAULT + BOLD
            elif "renamed" in file_status:
                line_color = DEFAULT + BOLD
            elif "type_changed" in file_status:
                line_color = DEFAULT + BOLD
            else:
                line_color = DEFAULT
            ret.append(f"{line_color}{file_status}{DEFAULT}")
    return "".join(ret)


def handle_print_status(git_return: str):
    branch_stage, conflits, files_track_stage, has_conflit = get_status_parts(git_return)
    print(build_new_status(branch_stage, conflits, files_track_stage, has_conflit))
