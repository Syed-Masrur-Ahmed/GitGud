"""Resolve divergent branch situations with AI guidance."""

import click
import inquirer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from gitgud.services.git.git_service import GitService
from gitgud.services.git.context_builder import ContextBuilder

console = Console()

@click.command()
def resolve():
    """Resolve divergent branches with interactive guidance.
    
    When your branch and the remote have diverged (both have unique commits),
    this command helps you understand the situation and choose the best resolution:
    
    - Explains what happened in plain English
    - Shows all your options (rebase, merge, force push)
    - Provides pros/cons for each approach
    - Gives AI-powered recommendations
    - Walks through execution step-by-step
    
    Perfect for when you're stuck and don't know what to do!
    
    Examples:
        gitgud resolve           # Interactive divergence resolution
    """
    git = GitService()
    
    if not git.is_git_repository():
        console.print("[red]Error: Not in a git repository[/red]")
        raise click.Abort()
    
    console.print("\n[bold cyan]GitGud Branch Resolver[/bold cyan]\n")
    
    # Build context
    with console.status("[bold green]Analyzing branches..."):
        context_builder = ContextBuilder(git)
        context = context_builder.build_context()
        branch_info = git.get_branch_info()
    
    if not context or not branch_info:
        console.print("[red]Failed to analyze repository[/red]")
        raise click.Abort()
    
    # Check if divergent
    if not branch_info.is_divergent:
        console.print("[green]OK: Your branch is not divergent![/green]")
        if branch_info.behind > 0:
            console.print("[yellow]Tip: You're behind. Run:[/yellow] [cyan]git pull[/cyan]")
        elif branch_info.ahead > 0:
            console.print("[yellow]Tip: You're ahead. Run:[/yellow] [cyan]git push[/cyan]")
        else:
            console.print("[green]Everything is synced![/green]")
        console.print()
        return
    
    # Show divergence situation
    console.print("[bold red]Branch Divergence Detected[/bold red]\n")
    
    # Create visual tree
    tree = Tree("[bold]Branch State[/bold]")
    
    local_branch = tree.add(f"[cyan]Local: {branch_info.local}[/cyan]")
    local_branch.add(f"[green]{branch_info.ahead} commits ahead[/green]")
    if context.uncommitted_changes > 0:
        local_branch.add(f"[yellow]{context.uncommitted_changes} uncommitted changes[/yellow]")
    
    remote_branch = tree.add(f"[blue]Remote: {branch_info.remote}[/blue]")
    remote_branch.add(f"[yellow]{branch_info.behind} commits you don't have[/yellow]")
    
    console.print(tree)
    console.print()
    
    # Show the problem
    explanation = f"""[bold]What happened:[/bold]

You have [green]{branch_info.ahead} local commit(s)[/green] that aren't on the remote.
Your teammate pushed [yellow]{branch_info.behind} commit(s)[/yellow] that you don't have.

Both branches have unique commits - this is called [red]"divergence"[/red].
Git can't automatically decide how to merge these."""
    
    console.print(Panel(explanation, border_style="yellow", padding=(1, 2)))
    console.print()
    
    # Show options
    console.print("[bold cyan]Your Options:[/bold cyan]\n")
    
    options_table = Table(show_header=True, header_style="bold cyan", box=None)
    options_table.add_column("Option", style="cyan", width=25)
    options_table.add_column("Pros", style="green", width=30)
    options_table.add_column("Cons", style="yellow", width=30)
    
    options_table.add_row(
        "1. Pull --rebase",
        "+ Clean history\n+ Linear timeline",
        "- May cause conflicts\n- Rewrites your commits"
    )
    options_table.add_row(
        "2. Pull (merge)",
        "+ Safe & simple\n+ Preserves all history",
        "- Creates merge commit\n- Messier history"
    )
    options_table.add_row(
        "3. Force push",
        "+ Overwrites remote\n+ Your version wins",
        "! DELETES teammate's work\n! Very dangerous!"
    )
    
    console.print(options_table)
    console.print()
    
    # AI/Heuristic recommendation
    recommendation = _get_recommendation(context, branch_info)
    console.print(Panel(
        f"[bold]Recommendation:[/bold] {recommendation}",
        border_style="blue",
        padding=(1, 2)
    ))
    console.print()
    
    # Interactive choice
    questions = [
        inquirer.List('action',
                     message="How would you like to resolve this?",
                     choices=[
                         ('Pull with rebase (keeps history clean)', 'rebase'),
                         ('Pull with merge (safer, creates merge commit)', 'merge'),
                         ('Cancel (I\'ll do it manually)', 'cancel'),
                     ],
                     default='rebase'),
    ]
    
    answers = inquirer.prompt(questions)
    
    if not answers or answers['action'] == 'cancel':
        console.print("\n[dim]Cancelled. No changes made.[/dim]\n")
        return
    
    # Handle uncommitted changes
    need_stash = context.uncommitted_changes > 0
    if need_stash:
        console.print("\n[yellow]WARNING: You have uncommitted changes. Will stash them first.[/yellow]")
        questions = [
            inquirer.Confirm('continue',
                           message="Continue?",
                           default=True),
        ]
        if not inquirer.prompt(questions)['continue']:
            console.print("\n[dim]Cancelled.[/dim]\n")
            return
    
    # Execute resolution
    console.print(f"\n[bold green]Executing resolution...[/bold green]\n")
    
    try:
        if need_stash:
            with console.status("[cyan]Stashing changes...[/cyan]"):
                git.execute_command("git stash")
            console.print("[green][OK][/green] Changes stashed")
        
        if answers['action'] == 'rebase':
            with console.status("[cyan]Pulling with rebase...[/cyan]"):
                success = git.execute_command("git pull --rebase")
        else:  # merge
            with console.status("[cyan]Pulling with merge...[/cyan]"):
                success = git.execute_command("git pull")
        
        if not success:
            console.print("[red][FAIL][/red] [red]Pull failed[/red]")
            console.print("\n[yellow]You may have conflicts. Run [cyan]git status[/cyan] to see them.[/yellow]\n")
            if need_stash:
                console.print("[yellow]Your changes are still in the stash. Run [cyan]git stash pop[/cyan] when ready.[/yellow]\n")
            raise click.Abort()
        
        console.print("[green][OK][/green] Pull successful")
        
        if need_stash:
            with console.status("[cyan]Restoring your changes...[/cyan]"):
                git.execute_command("git stash pop")
            console.print("[green][OK][/green] Changes restored")
        
        console.print("\n[bold green]Resolution complete![/bold green]")
        console.print("[dim]Your branch is now synced with remote.[/dim]\n")
        
        # Ask about pushing
        questions = [
            inquirer.Confirm('push',
                           message="Push your changes now?",
                           default=True),
        ]
        if inquirer.prompt(questions)['push']:
            with console.status("[cyan]Pushing...[/cyan]"):
                git.execute_command("git push")
            console.print("[green][OK][/green] [bold]Pushed successfully![/bold]\n")
        
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]\n")
        raise click.Abort()


def _get_recommendation(context, branch_info) -> str:
    """Get recommendation based on context."""
    # Simple heuristic for now
    if branch_info.behind <= 2 and branch_info.ahead <= 2:
        return "git pull --rebase\n\nBoth branches have few commits. Rebase will likely work smoothly."
    elif branch_info.behind > 5:
        return "git pull (merge)\n\nRemote has many commits. Merge is safer to avoid complex rebase conflicts."
    else:
        return "git pull --rebase\n\nRebase recommended to keep history clean."

