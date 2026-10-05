import main.config as config
import os
import shutil
import subprocess
import sys
import time

# colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Notes: refuse to run from the home directory before performing other work.
current_directory = os.path.realpath(os.getcwd())
home_directory = os.path.realpath(os.path.expanduser("~"))
if current_directory == home_directory:
    print(f"{RED}Easy Git can't run in your home directory.{RESET}")
    sys.exit(1)

# Notes: check config directly. Importing setup.py would run setup again.
if not config.is_configured():
    print(f"{RED}Error 001. Run the error file to check the reason.{RESET}")
    sys.exit(1)

else:
    # Notes: show progress for the real startup checks instead of a timed spinner.
    stages = ["Checking setup", "Checking current folder", "Loading command menu"]
    total = len(stages)
    for loaded, stage in enumerate(stages, start=1):
        block = "█" * loaded
        empty = "-" * (total - loaded)
        print(f"\r({block}{empty}) {loaded}/{total} {stage}\033[K", end="", flush=True)
        if stage == "Checking current folder":
            current_directory = os.path.realpath(os.getcwd())
        time.sleep(0.15)
    print("\r\033[K", end="", flush=True)

    # Notes: display the current folder and check for an existing repository.
    print(f"Current folder: {os.path.basename(current_directory)}")
    if os.path.exists(os.path.join(current_directory, ".git")):
        # Notes: an existing repository needs no setup; continue directly to the menu.
        pass
    else:
        # -------------------------------- Repository setup --------------------------------
        choice = input(
            "Git is not initialized in this folder. Set it up now? (y/n): "
        ).strip().lower()
        if choice != "y":
            print(f"{RED}Git setup was declined. Exiting.{RESET}")
            sys.exit(1)

        # Notes: collect repository details before changing anything.
        default_name = os.path.basename(current_directory)
        repo_name = input(f"Repository name [{default_name}]: ").strip() or default_name
        visibility = input("Public or private? (public/private) [private]: ").strip().lower()
        visibility = visibility or "private"
        description = input("Repository description (optional): ").strip()
        if visibility not in ("public", "private"):
            print(f"{RED}Choose public or private. No changes were made.{RESET}")
            sys.exit(1)

        # Notes: initialize the local Git repository.
        try:
            subprocess.run(
                ["git", "init", "-b", "main"],
                cwd=current_directory,
                check=True,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError:
            print(f"{RED}Git is not installed. Repository setup could not start.{RESET}")
            sys.exit(1)
        except subprocess.CalledProcessError as error:
            print(f"{RED}Git initialization failed: {error.stderr.strip()}{RESET}")
            sys.exit(1)

        # Notes: create a hosted GitHub repository when GitHub CLI is available.
        remote_report = "No hosted repository was created."
        if shutil.which("gh"):
            command = [
                "gh", "repo", "create", repo_name,
                f"--{visibility}", "--source", current_directory,
                "--remote", "origin",
            ]
            if description:
                command.extend(["--description", description])
            try:
                subprocess.run(
                    command,
                    cwd=current_directory,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                remote_report = f"GitHub repository created as {visibility} (remote: origin)."
            except subprocess.CalledProcessError as error:
                details = error.stderr.strip() or error.stdout.strip()
                remote_report = f"GitHub creation failed: {details or 'see GitHub CLI output.'}"
        else:
            remote_report = "GitHub CLI (gh) is unavailable; only the local repository was created."

        # Notes: report local and hosted setup results.
        print(f"{GREEN}Setup report:{RESET}")
        print("  Local Git repository: initialized")
        print("  Branch: main")
        print(f"  Repository name: {repo_name}")
        print(f"  Requested visibility: {visibility}")
        print(f"  Hosted repository: {remote_report}")
        # wait for user acknowledgment before proceeding to the interactive menu.
        input("Press Enter to continue...")

    # ----------------------------------- Command menu -----------------------------------
    # Notes: both existing and newly initialized repositories continue to the menu.
    # Clear the terminal before launching the menu.
    os.system("cls" if os.name == "nt" else "clear")

    print("Pick an option from the menu:")
    print("  1. Git status")
    print("  2. Git add")
    print("  3. Git ignore")
    print("  4. Git commit")
    print("  5. Git push")
    print("  6. Git pull")
    print("  7. Git branch")
    print("  8. Exit")

    choice = input("Enter your choice: ").strip()
    if choice == "1":
        subprocess.run(["git", "status"], cwd=current_directory)
    elif choice == "2":
        subprocess.run(["git", "add", "."], cwd=current_directory)
    elif choice == "3":
        ignore_file = input("Enter the name of the file to ignore: ").strip()
        subprocess.run(["git", "ignore", ignore_file], cwd=current_directory)
    elif choice == "4":
        commit_message = input("Enter commit message: ").strip()
        subprocess.run(["git", "commit", "-m", commit_message], cwd=current_directory)
    elif choice == "5":
        subprocess.run(["git", "push", "origin", "main"], cwd=current_directory)
    elif choice == "6":
        subprocess.run(["git", "pull", "origin", "main"], cwd=current_directory)
    elif choice == "7":
        subprocess.run(["git", "branch"], cwd=current_directory)
    elif choice == "8":
        print("Exiting...")
        sys.exit(0)
    else:
        print(f"{RED}Invalid choice. Please try again.{RESET}")
    input("Press Enter to continue...")  # Pause before showing the menu again
    os.system("cls" if os.name == "nt" else "clear")  # Clear the terminal for the next menu display
