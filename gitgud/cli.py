import click
from rich.console import Console
from gitgud.commands.status import status
from gitgud.commands.push import push

console = Console()

@click.group()
@click.version_option(version="1.0.0")
def main():
    """GitGud - AI-powered Git assistant."""
    pass

@main.command()
def test():
    """Test if GitGud is working."""
    console.print("[green]✅ GitGud is working![/green]")
    console.print("[blue]🚀 Ready to make Git easy![/blue]")

# Register commands
main.add_command(status)
main.add_command(push)

if __name__ == "__main__":
    main()