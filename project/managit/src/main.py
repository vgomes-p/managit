import argparse
from packaging import version
import pkg_resources
import sys
from managit.src.managitshell import managit_shell

def main():
    parser = argparse.ArgumentParser(description="Managit - your personal git manager!")
    parser.add_argument("--version", action="store_true", help="Display program's version")
    parser.add_argument("--start", action="store_true", help="Force to start the program (you can start the program just with program name as well!)")

    args = parser.parse_args()

    if args.version:
        version_check = pkg_resources.get_distribution("managit").version
        print(f"managit version: {version_check}")
        sys.exit(0)
    else:
        managit_shell()

if __name__ == "__main__":
    main()