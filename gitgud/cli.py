import click
from rich.console import Console
from gitgud.commands.status import status
from gitgud.commands.push import push
from gitgud.commands.resolve import resolve
from gitgud.commands.commit import commit

console = Console()

@click.group()
@click.version_option(version="1.0.0")
def main():
    """GitGud - AI-powered Git assistant.
    
    Makes Git operations effortless with intelligent analysis and recommendations.
    Uses AI (Ollama + CodeLlama) with rule-based fallback for reliability.
    
    Commands:
        status      Show repository health dashboard
        commit      Smart commit with AI-generated messages
        push        Smart push with AI analysis
        resolve     Resolve divergent branches interactively
    
    Examples:
        gitgud status           # Check repository health
        gitgud commit           # Commit with AI message
        gitgud push             # Intelligent push
        gitgud resolve          # Fix divergent branches
        gitgud --help           # Show this message
    """
    pass

@main.command()
def test():
    """Test if GitGud is working."""
    console.print("[green]OK: GitGud is working![/green]")
    console.print("[blue]Ready to make Git easy![/blue]")

# Register commands
main.add_command(status)
main.add_command(commit)
main.add_command(push)
main.add_command(resolve)

if __name__ == "__main__":
    main()