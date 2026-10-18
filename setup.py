import json
import subprocess
import sys
import time
from pathlib import Path

from rich.console import Console
from rich.progress import Progress
from rich.prompt import Prompt


console = Console()
config_path = Path(__file__).with_name("config.json")


def load_config():
    # Treat a missing or empty config file as a first-time setup.
    try:
        with config_path.open("r", encoding="utf-8") as config_file:
            config = json.load(config_file)
    except (FileNotFoundError, json.JSONDecodeError):
        config = {}

    return config if isinstance(config, dict) else {}


def command_output(command):
    # Return command output while allowing callers to handle command failures.
    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() or result.stderr.strip()


def main():
    config = load_config()

    if config.get("setup", False):
        console.print("Setup is complete")
        return

    with Progress() as progress:
        # Run the required environment checks before saving setup state.
        task = progress.add_task("Setting up...", total=3)
        time.sleep(1)

        try:
            command_output(["git", "--version"])
            progress.advance(task)
        except (FileNotFoundError, subprocess.CalledProcessError):
            console.print("Git is not installed")
            return

        try:
            git_user = command_output(["git", "config", "--get", "user.name"])
            if not git_user:
                raise subprocess.CalledProcessError(1, ["git", "config"])
            progress.advance(task)
        except (FileNotFoundError, subprocess.CalledProcessError):
            console.print("Git is not configured")
            return

        try:
            github_status = command_output(["gh", "auth", "status"])
            progress.advance(task)
        except (FileNotFoundError, subprocess.CalledProcessError):
            console.print("GitHub is not authenticated")
            return

    # Save setup state only after every check succeeds.
    config["setup"] = True
    with config_path.open("w", encoding="utf-8") as config_file:
        json.dump(config, config_file, indent=2)
        config_file.write("\n")

    console.print("Setup is complete", style="bold white")
    try:
        response = Prompt.ask(
            "Would you like to see the report of info?",
            choices=["Y", "n"],
            default="n",
        )
    except EOFError:
        # Skip the optional report when no interactive input is available.
        response = "n"
    if response == "Y":
        console.print(f"Git info: {git_user}")
        console.print(f"GitHub info: {github_status}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("Setup cancelled")
        sys.exit(130)
    
