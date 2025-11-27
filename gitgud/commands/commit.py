"""Smart commit command with AI-generated messages."""

import click
import inquirer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from gitgud.services.git.git_service import GitService
from gitgud.services.ai.commit_message_generator import CommitMessageGenerator

console = Console()

@click.command()
@click.option('-m', '--message', help='Commit message (skips AI generation)')
@click.option('--ai', is_flag=True, help='Force AI generation even with -m')
@click.option('--no-ai', is_flag=True, help='Skip AI, prompt for manual message')
def commit(message, ai, no_ai):
    """Smart commit with optional AI-generated messages.
    
    Stages changes and creates a commit. Can generate commit messages
    using AI (Ollama) by analyzing your changes.
    
    Modes:
    - Default: Interactive - asks if you want AI to generate message
    - With -m: Uses your message directly
    - With --ai: Forces AI generation (analyzes and suggests message)
    - With --no-ai: Prompts for manual message entry
    
    Examples:
        gitgud commit                    # Interactive mode
        gitgud commit --ai               # AI generates message
        gitgud commit --no-ai            # Manual message entry
        gitgud commit -m "fix: bug"      # Direct message
    """
    git = GitService()
    
    if not git.is_git_repository():
        console.print("[red]Error: Not in a git repository[/red]")
        raise click.Abort()
    
    console.print("\n[bold cyan]GitGud Smart Commit[/bold cyan]\n")
    
    # Check for changes to commit
    status = git.get_status()
    if not status:
        console.print("[red]Error: Could not get repository status[/red]")
        raise click.Abort()
    
    # Check for staged or modified files
    has_changes = status.modified > 0 or status.created > 0
    
    if not has_changes:
        console.print("[yellow]No changes to commit[/yellow]")
        console.print("[dim]Working tree is clean[/dim]\n")
        return
    
    # Show what will be committed
    console.print("[bold]Changes to be committed:[/bold]")
    console.print(f"  Modified:  {status.modified} files")
    console.print(f"  Untracked: {status.created} files")
    console.print()
    
    # Get diff for AI analysis
    with console.status("[dim]Getting changes...[/dim]"):
        diff = _get_diff(git)
    
    if not diff:
        console.print("[yellow]No changes detected in diff[/yellow]\n")
        return
    
    # Determine message source
    commit_message = None
    
    if message and not ai:
        # User provided message with -m
        commit_message = message
        console.print(f"[bold]Using provided message:[/bold] {message}\n")
    
    elif no_ai:
        # Manual entry requested
        commit_message = _prompt_manual_message()
        if not commit_message:
            console.print("\n[dim]Commit cancelled[/dim]\n")
            return
    
    else:
        # AI generation (default or --ai flag)
        console.print("[bold]Generating commit message with AI...[/bold]\n")
        
        generator = CommitMessageGenerator()
        
        with console.status("[cyan]Analyzing changes...[/cyan]"):
            generated_message = generator.generate(diff, status)
        
        if not generated_message:
            console.print("[yellow]AI generation failed. Falling back to manual entry.[/yellow]\n")
            commit_message = _prompt_manual_message()
            if not commit_message:
                console.print("\n[dim]Commit cancelled[/dim]\n")
                return
        else:
            # Show generated message
            console.print("[bold]Generated commit message:[/bold]")
            console.print(Panel(
                generated_message,
                border_style="green",
                padding=(1, 2)
            ))
            console.print()
            
            # Ask for approval
            questions = [
                inquirer.List('action',
                             message="What would you like to do?",
                             choices=[
                                 ('Use this message', 'use'),
                                 ('Edit message', 'edit'),
                                 ('Enter manually', 'manual'),
                                 ('Cancel', 'cancel'),
                             ],
                             default='use'),
            ]
            
            answer = inquirer.prompt(questions)
            
            if not answer or answer['action'] == 'cancel':
                console.print("\n[dim]Commit cancelled[/dim]\n")
                return
            elif answer['action'] == 'use':
                commit_message = generated_message
            elif answer['action'] == 'edit':
                console.print("\n[dim]Opening editor to edit message...[/dim]")
                commit_message = _edit_message(generated_message)
                if not commit_message:
                    console.print("\n[dim]Commit cancelled[/dim]\n")
                    return
            else:  # manual
                commit_message = _prompt_manual_message()
                if not commit_message:
                    console.print("\n[dim]Commit cancelled[/dim]\n")
                    return
    
    # Stage all changes
    console.print()
    with console.status("[cyan]Staging changes...[/cyan]"):
        try:
            if git.repo:
                git.repo.git.add('-A')
                success = True
            else:
                success = False
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            success = False
    
    if not success:
        console.print("[red][FAIL][/red] Failed to stage changes\n")
        raise click.Abort()
    
    console.print("[green][OK][/green] Changes staged")
    
    # Create commit using GitPython directly (safer than shell command)
    with console.status("[cyan]Creating commit...[/cyan]"):
        try:
            if git.repo:
                git.repo.index.commit(commit_message)
                success = True
            else:
                success = False
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            success = False
    
    if success:
        console.print("[green][OK][/green] Commit created")
        console.print(f"\n[bold green]Success![/bold green] Changes committed.\n")
    else:
        console.print("[red][FAIL][/red] Commit failed\n")
        raise click.Abort()


def _get_diff(git: GitService) -> str:
    """Get diff of changes."""
    try:
        # Get diff of unstaged changes
        if git.repo:
            diff = git.repo.git.diff()
            # Also get untracked files
            untracked = git.repo.untracked_files
            if untracked:
                diff += f"\n\nUntracked files:\n" + "\n".join(f"  {f}" for f in untracked)
            return diff if diff else ""
    except Exception:
        return ""
    return ""


def _prompt_manual_message() -> str:
    """Prompt user for manual message entry."""
    questions = [
        inquirer.Text('message',
                     message="Enter commit message",
                     validate=lambda _, x: len(x.strip()) > 0 or "Message cannot be empty"),
    ]
    
    answer = inquirer.prompt(questions)
    return answer['message'].strip() if answer else ""


def _edit_message(initial_message: str) -> str:
    """Open editor to edit message."""
    import tempfile
    import subprocess
    import os
    
    # Create temporary file with message
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(initial_message)
        temp_path = f.name
    
    try:
        # Open in editor
        editor = os.environ.get('EDITOR', 'vim')
        subprocess.call([editor, temp_path])
        
        # Read edited message
        with open(temp_path, 'r') as f:
            edited = f.read().strip()
        
        return edited
    finally:
        # Clean up
        os.unlink(temp_path)

