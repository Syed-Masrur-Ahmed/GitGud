import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from gitgud.services.git.git_service import GitService

console = Console()

@click.command()
def status():
    """Show repository health dashboard.
    
    Displays a beautiful terminal dashboard with:
    - Current branch and remote tracking status
    - Commits ahead/behind remote
    - Uncommitted and untracked files
    - Overall repository health indicator
    
    Examples:
        gitgud status
    """
    git = GitService()
    
    if not git.is_git_repository():
        console.print("[red]Error: Not in a git repository[/red]")
        console.print("[dim]Run this command inside a git repository[/dim]")
        raise click.Abort()
    
    with console.status("[bold green]Analyzing repository..."):
        git.fetch()
        status = git.get_status()
        branch_info = git.get_branch_info()
    
    if not status or not branch_info:
        console.print("[red]Failed to get repository status[/red]")
        raise click.Abort()
    
    # Determine status indicator
    if branch_info.is_divergent:
        status_indicator = "[!]"
        status_text = "DIVERGENT"
        status_color = "red"
    elif branch_info.behind > 0:
        status_indicator = "[*]"
        status_text = "NEEDS SYNC"
        status_color = "yellow"
    elif not status.is_clean:
        status_indicator = "[*]"
        status_text = "UNCOMMITTED CHANGES"
        status_color = "yellow"
    else:
        status_indicator = "[OK]"
        status_text = "CLEAN"
        status_color = "green"
    
    # Create table
    table = Table(title="Repository Health", show_header=False, box=None)
    table.add_column("Label", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Repository", str(git.path.resolve().name))
    table.add_row("Branch", status.current)
    if status.tracking:
        table.add_row("Remote", status.tracking)
    else:
        table.add_row("Remote", "[dim]No tracking branch[/dim]")
    table.add_row("", "")
    table.add_row(f"Status", f"{status_indicator} [{status_color}]{status_text}[/{status_color}]")
    table.add_row("", "")
    table.add_row("Commits", "")
    table.add_row("  Ahead", f"[green]{branch_info.ahead}[/green] commits")
    table.add_row("  Behind", f"[yellow]{branch_info.behind}[/yellow] commits")
    table.add_row("", "")
    table.add_row("Changes", "")
    table.add_row("  Modified", f"{status.modified} files")
    table.add_row("  Untracked", f"{status.created} files")
    
    panel = Panel(table, border_style="cyan", padding=(1, 2))
    console.print("\n", panel, "\n")
    
    # Suggestions
    if not status.tracking and status.current != "HEAD (detached)":
        console.print("[yellow]Tip:[/yellow] No tracking branch set. Push with [cyan]git push -u origin " + status.current + "[/cyan]\n")
    elif branch_info.ahead > 0:
        console.print("[blue]Suggestion:[/blue] Run [bold]gitgud push[/bold] to sync with remote\n")