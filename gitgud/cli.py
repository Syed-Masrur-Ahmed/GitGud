import click
from rich.console import Console
from gitgud.commands.status import status
from gitgud.commands.push import push
from gitgud.commands.resolve import resolve
from gitgud.commands.commit import commit

console = Console()

ASCII_ART = """
[bold bright_magenta]  ██████  ██ ████████  ██████  ██    ██ ██████  [/bold bright_magenta]
[bright_magenta] ██       ██    ██    ██       ██    ██ ██   ██ [/bright_magenta]
[magenta] ██   ███ ██    ██    ██   ███ ██    ██ ██   ██ [/magenta]
[magenta] ██    ██ ██    ██    ██    ██ ██    ██ ██   ██ [/magenta]
[magenta]  ██████  ██    ██     ██████   ██████  ██████  [/magenta]

[dim]        AI-Powered Git Assistant[/dim]
"""

class CustomGroup(click.Group):
    """Custom click group that shows ASCII art with help."""
    
    def format_help(self, ctx, formatter):
        """Override format_help to add ASCII art."""
        # Print ASCII art first (using console)
        console.print(ASCII_ART)
        # Then show regular help
        super().format_help(ctx, formatter)

@click.group(cls=CustomGroup, invoke_without_command=True)
@click.pass_context
@click.version_option(version="1.0.0")
def main(ctx):
    """
    GitGud - AI-powered Git assistant.

    Makes Git operations effortless with intelligent analysis and recommendations.
    Uses AI (Ollama + CodeLlama) with rule-based fallback for reliability.

    \b
    Commands:
      status      Show repository health dashboard
      commit      Smart commit with AI-generated messages
      push        Smart push with AI analysis
      resolve     Resolve divergent branches interactively

    \b
    Examples:
      gitgud status           # Check repository health
      gitgud commit           # Commit with AI message
      gitgud push             # Intelligent push
      gitgud resolve          # Fix divergent branches
      gitgud --help           # Show this message
    """
    # Show help when no command given
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())
        ctx.exit()

@main.command()
def test():
    """Test if GitGud is working."""
    console.print(ASCII_ART)
    console.print("[green]OK: GitGud is working![/green]")
    console.print("[blue]Ready to make Git easy![/blue]")

# Register commands
main.add_command(status)
main.add_command(commit)
main.add_command(push)
main.add_command(resolve)

if __name__ == "__main__":
    main()