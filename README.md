# ManaGit | Your Personal Git Manager 🚀
![ManaGit | Your Personal Git Manager](src/intro.png)


### ManaGit is a CLI tool designed to manage and automate workflows across multiple Git repositories from a single interface.

### It provides both command-line options and an interactive shell to streamline repository maintenance, updates, and status tracking.

![ManaGit working on commiting mode](src/commiting.png)

## Features
- **Interactive shell** with a clean, colorful interface
- `pull`
- `status`
- `add`
- `commit`
- `push`
- `branch`
- Some shell commands
- Safe signal handling (blocks Ctrl+C inside the shell)

## Installation

### Install as package (sudo permission needed):
```Bash
cd project
make install
```

### Install as alias:
#### 1. Prepare the enviroment
```bash
make create-env
```

#### 2. Create the alias
##### 2.1 - Open your shell rc file (example with bash)
```bash
nano ~/.bashrc
```

##### 2.2 Pass the alias to your 
> remember to change `"python3"` with you python interpreter
```bash
alias py="python3"
alias managit="py ~/.managit/program/managit/src/run_managit.py"
```

##### 2.3 Save the changes
```bash
CTRL^X
Y
ENTER
```

##### 2.4 - Update
```bash
source ~/.bashrc
```

#### 3. Call it
```bash
managit
```
> This will not install managit as a package, so if you need to update it, you can go to repository with `cd ~/.managit`and run pull or create the alias managit-update (intructions in the end of the README).

### Usage
Simply run:
```Bash
managit
```
Or (if installed as package):
```Bash
managit --start
```
#### Check the ManaGit preview:
[![Preview ManaGit](https://img.shields.io/badge/Preview%20ManaGit-blue?style=for-the-badge)](PREVIEW.md)

## Commands inside the shell

- pull — Pull latest changes from remote
- add — Add the intructed files to track
- commit — Check untracked files and run commit message creator
- push — Push to remote (asks if you want --force)
- branch — create a new branch copying the main
- clear — Clear terminal screen
- cd — Navigate into repositories (also works just entering the path)
- ls — show files in the current path
- exit — Exit managit

## Upcoming features
- New colors
- `deconflit` — to fix conflit between local and remote repository
- `config` — to configure git user data
- `restore` — to restore local repository
- `clone` — to clone repository
- `env_checker()` — do now allow commit with .env in track

## Project Structure
```text
managit/project/
├─ 📁 program
│  ├─ 📁 managit
│  │  ├─ 📁 src
│  │  │  ├─ 🐍 __init__.py
│  │  │  ├─ 🐍 get_commit_info.py
│  │  │  ├─ 🐍 git_cmds.py
│  │  │  ├─ 🐍 main.py
│  │  │  ├─ 🐍 managitshell.py
│  │  │  ├─ 🐍 parser_git_status.py
│  │  │  ├─ 🐍 run_managit.py
│  │  │  ├─ 🐍 shell_cmds.py
│  │  │  └─ 🐍 shells_prompt.py
│  │  ├─ 📁 utils
│  │  │  ├─ 🐍 __init__.py
│  │  │  ├─ 🐍 clear.py
│  │  │  ├─ 🐍 colors.py
│  │  │  └─ 🐍 nbr.py
│  │  └─ 🐍 __init__.py
│  ├─ 📄 Makefile
│  ├─ 🐍 setup.py
│  └─ 🐍 setup.py
├─ 📁 src
│  └─ 🖼️ *.png
├─ ⚙️ .gitignore
├─ 📄 LICENSE
├─ 📝 PREVIEW.md
└─ 📝 README.md
```

## Tech Stack

Python 3.6+
setuptools for packaging
subprocess for Git integration
Custom colored terminal output

## License
This project is licensed under the MIT License — see the LICENSE file for details.

## Author
Made by Vinny (@vgomes-p)

## Happy coding!
Feel free to open issues or submit PRs.