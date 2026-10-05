import time
import main.config as config
from pathlib import Path
import os
import subprocess


# Mistake fixed: the old script set setup_done to True and then used a separate
# if statement, so it printed "already completed" on the first successful run.
# This if/else checks the status from config once: an existing flag means setup
# was done on an earlier run; otherwise, show progress and save the flag.
if config.setup_done:
    RED = "\033[91m"
    print(f"{RED}Setup has already been completed.{RED}")
else:
    # Set the number of steps represented by the progress bar.
    total = 20

    # Update the progress bar for every step, including the completed state.
    for loaded in range(total + 1):
        # Use solid blocks for completed steps and dashes for remaining steps.
        GREEN = "\033[92m"
        block = ("█") * loaded
        empty = "-" * (total - loaded)

        # Return to the start of the same line and show the current step count.
        # Keep the line open and flush output so each update appears immediately.
        print(f"\r({block}{empty}) {loaded}/{total}", end="", flush=True)
        # Pause between updates so the animation can be seen.
        # Make it delete after the final step to clean up the progress bar.
        if loaded == total:
            print("\r" + " " * (total + 10) + "\r", end="", flush=True)
        time.sleep(0.1)

    # Save the flag only after setup finishes; config.py reads it next time.
    with config.SETUP_FLAG.open("w", encoding="utf-8") as flag_file:
        flag_file.write("done\n")
    GREEN = "\033[92m"
    RED = "\033[91m"
    if Path.cwd() == Path.home():
        print(f"{RED}Error 002.{RED}")

    git_config = Path.home() / ".gitconfig"
    if git_config.exists():
        print("Would you like the program to run: install.sh? (y/n): ", end="")
        if input().strip().lower() == "y":
            subprocess.run(["bash", "install.sh"])
            # Check if failed to run.
            if subprocess.run(["bash", "install.sh"]).returncode != 0:
                print(f"{RED}Error 004.{RED}")
                exit(1)

            else:
                print(f"{GREEN}install.sh ran successfully.{GREEN}")
                print("Would you like to see the commands? (y/n): ", end="")
                if input ().strip().lower() == "y":
                    subprocess.run(["bash", "install.sh", "--show-commands"])

    else:
        # Check if there signed into Git
        if not git_config.exists():
            print(f"{RED}Error 003.{RED}")
        
