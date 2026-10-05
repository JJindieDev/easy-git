import sys
import time

# Note: Keep config optional; importing a missing config module previously stopped
# execution before load_errors() could return its fallback error dictionary.
try:
    import main.config as config
except ImportError:
    config = None

# Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def load_errors():
    errors = getattr(config, "ERRORS", None)
    if not isinstance(errors, dict):
        errors = {"001": "This error is related to incomplete setup."}
        errors["002"] = "This error is related to being in the home directory during setup."
        errors["003"] = "This error is related to not being signed into Git. Or git is not initialized in the current folder."
    return errors


# Note: Edit this list to customize the loading stages. Keep TESTING if it is
# needed; the progress bar calculates its total from this list automatically.
steps = ["Reading config", "Loading errors", "Finalizing"]
total = len(steps)
errors = {}

# Note: Edit the sleep duration below to change loading speed. range(total + 1)
# includes the completed state, so preserve it when changing the loading system.
for loaded in range(total + 1):
    block = "█" * loaded
    empty = "-" * (total - loaded)
    label = steps[loaded - 1] if loaded > 0 else "Starting"

    if loaded == 2:
        errors = load_errors()

    # \033[K clears the rest of the line to avoid leftover text.
    print(f"\r({GREEN}{block}{RESET}{empty}) {loaded}/{total} {label}\033[K", end="", flush=True)
    time.sleep(0.5)

# Remove the loading bar once done.
print("\r\033[K", end="", flush=True)

try:
    error_number = input("What error would you like to check? ").strip()
except KeyboardInterrupt:
    print("\nInput cancelled.")
    sys.exit(0)

print(f"Checking for error: {error_number}")
if error_number in errors:
    print(f"{YELLOW}{errors[error_number]}{RESET}")
else:
    print(f"{RED}Unknown error number.{RESET}")
        