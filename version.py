# when ran it should print the version of the program
from rich.console import Console
from rich.text import Text
# make the easy git text bold white

console = Console()
version = Text("Easy Git v0.0.1", style="dim white")
console.print(version)
