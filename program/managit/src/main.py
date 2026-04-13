from managit.src.managitshell import managit_shell
from packaging import version
import pkg_resources
import argparse
import subprocess
import shutil
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="Managit - your personal git manager!")
    parser.add_argument("--version", action="store_true", help="Display program's version")
    parser.add_argument("--start", action="store_true", help="Force to start the program (you can start the program just with program name as well!)")
    parser.add_argument("--update", action="store_true", help="Update the program")
    parser.add_argument("--fix", action="store_true", help="Fix if the program branch is different than 'main'")
    parser.add_argument("--find", action="store_true", help="Checks is ~/.managit")
    parser.add_argument("--reinstall", action="store_true", help="Reinstall the program.")
    parser.add_argument("--uninstall", action="store_true", help="Show the steps to uninstall managit.")

    args = parser.parse_args()

    if args.version:
        version_check = pkg_resources.get_distribution("managit").version
        print(f"managit version: {version_check}")
        sys.exit(0)
    elif args.update:
        update()
        sys.exit(0)
    elif args.fix:
        fix()
        sys.exit(0)
    elif args.find:
        find()
        sys.exit(0)
    elif args.reinstall:
        reinstall()
        sys.exit(0)
    elif args.uninstall:
        uninstall()
        sys.exit(0)
    else:
        managit_shell()
        sys.exit(0)

root = os.path.expanduser("~/.managit/")
program_files = os.path.expanduser("~/.managit/project/")

def pull_update():
    try:
        subprocess.run(["git", "pull", "origin", "main"],
                       cwd=root, check=True, text=True,
                       capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: pulling updates failed: {e.stderr if e.stderr else e}")
        if "There is no tracking information" in e.stderr:
            print("TIP: try run 'managit --fix'!")
    except FileNotFoundError:
        print("Error: Git not installed or not found in PATH.")
    except OSError as e:
        print("""Error: Failed to access '~/.managit'!
┌──────────────────────────────────────────────────────────────┐
│Possible solution:                                            │
┌──────────────────────────────────────────────────────────────┐
│Run 'managit --find', if it returns 'managit root not found', │
│run 'managit --reinstall'                                     │
└──────────────────────────────────────────────────────────────┘
""")
    pass


def fix():
    try:
        subprocess.run(["git", "branch", "--set-upstream-to=origin/main", "main"],
                       cwd=root, check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: failed to fix ~/.managit: {e.stderr if e.stderr else e}")
    except FileNotFoundError:
        print("Error: Git is not installed or not found in PATH.")
    except OSError as e:
        print(f"Error accessing repository directory: {e}")


def install():
    try:
        subprocess.run(["sudo", "pip", "install", "-e", ".", "--break-system-packages"],
                       cwd=program_files, check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: failed to install updates: {e.stderr if e.stderr else e}")
    except FileNotFoundError:
        print("Error: pip is not installed or not found in PATH.")
    except OSError as e:
        print(f"Error accessing repository directory: {e}")


def update():
    try:
        pull_update()
    except:
        print("Error: failed t updating...")
        return
    try:
        install()
        print("Updated installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: failed to install update: {e.stderr if e.stderr else e}")
    except FileNotFoundError:
        print("Error: pip is not installed or not found in PATH")
    except OSError as e:
        print(f"Error: failed to access '~/.managit': {e}")


def find():
    'cd ~ && [ -d ".managit" ] && echo "existe" || echo "não existe"'
    try:
        if os.path.isdir(os.path.expanduser("~/.managit")):
            print("found")
        else:
            print("not found")
    except:
        print("Error: failed to run --find.")
        return


def clone():
    home = os.path.expanduser("~")
    try:
        subprocess.run(["git", "clone", "https://github.com/vgomes-p/managit.git", ".managit"],
                       cwd=home, check=True, text=True, capture_output=True)
    except FileNotFoundError:
        print("Error: Git not installed or not found in PATH.")
    except:
        print("Error: failed to clone from 'https://github.com/vgomes-p/managit.git'.")
    return


manual = """┌──────────────────────────────────────────────────────────────┐
│Manual process:                                            │
┌──────────────────────────────────────────────────────────────┐
│cd ~                                                          │
│rm -rfd .managit                                              │
│git clone https://github.com/vgomes-p/managit.git ~/.managit  │
│cd .managit/program                                           │
│sudo pip install ~/.managit/program/. --break-system-packages │
└──────────────────────────────────────────────────────────────┘"""


def reinstall():
    to_rm = os.path.expanduser("~/.managit/")
    try:
        shutil.rmtree(to_rm, ignore_errors=True)
        clone()
        install()
        print("Installed successfully.")
    except:
        print("Error: failed to reinstall managit. Try to do is manually.\n")
        print(manual)
    return

def uninstall():
    print("Step 1: Run 'sudo pip uninstall managit --break-system-packages'.")
    print("Step 2: Run 'srm -rfd ~/.managit'.")


if __name__ == "__main__":
    main()
