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
@click.option('-m', '--message', help='Commit message (direct)')
@click.option('--ai', is_flag=True, help='Use AI to generate message (experimental)')
@click.option('--manual', is_flag=True, help='Prompt for manual message entry')
def commit(message, ai, manual):
    """Smart commit with heuristic-generated messages.
    
    Stages changes and creates a commit. By default uses smart heuristics
    to generate commit messages. Optionally can use AI (Ollama).
    
    Modes:
    - Default: Uses heuristic to generate message
    - With -m: Uses your message directly
    - With --ai: Uses AI (Ollama) to generate message (experimental)
    - With --manual: Prompts for manual message entry
    
    Examples:
        gitgud commit                    # Heuristic generation (default)
        gitgud commit --ai               # AI generation (experimental)
        gitgud commit --manual           # Manual entry
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
    
    # Warn about large commits
    total_files = status.modified + status.created
    if total_files > 100:
        console.print(f"\n[yellow]Warning: Committing {total_files} files at once![/yellow]")
        console.print("[dim]Consider breaking this into smaller commits[/dim]")
        if not click.confirm("\nContinue anyway?", default=False):
            console.print("[dim]Commit cancelled[/dim]\n")
            return
    
    console.print()
    
    # Get diff for AI analysis
    with console.status("[dim]Getting changes...[/dim]"):
        diff = _get_diff(git)
    
    if not diff:
        console.print("[yellow]No changes detected in diff[/yellow]\n")
        return
    
    # Determine message source
    commit_message = None
    
    if message:
        # User provided message with -m
        commit_message = message
        console.print(f"[bold]Using provided message:[/bold] {message}\n")
    
    elif manual:
        # Manual entry requested
        commit_message = _prompt_manual_message()
        if not commit_message:
            console.print("\n[dim]Commit cancelled[/dim]\n")
            return
    
    elif ai:
        # AI generation (experimental, opt-in)
        console.print("[bold]Generating commit message with AI...[/bold]\n")
        
        generator = CommitMessageGenerator()
        
        with console.status("[cyan]Analyzing changes...[/cyan]"):
            try:
                # Try AI first
                from gitgud.services.ai.ollama import OllamaProvider
                ollama = OllamaProvider()
                if ollama.is_available():
                    generated_message = generator._generate_with_ai(diff, status)
                else:
                    console.print("[yellow]AI not available, using heuristic...[/yellow]")
                    generated_message = generator._generate_heuristic(diff, status)
            except:
                console.print("[yellow]AI failed, using heuristic...[/yellow]")
                generated_message = generator._generate_heuristic(diff, status)
        
        if not generated_message:
            console.print("[yellow]Generation failed. Using manual entry.[/yellow]\n")
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
    
    else:
        # Default: Use heuristic generation (fast and reliable)
        console.print("[bold]Generating commit message...[/bold]\n")
        
        generator = CommitMessageGenerator()
        
        with console.status("[cyan]Analyzing changes...[/cyan]"):
            generated_message = generator._generate_heuristic(diff, status)
        
        if not generated_message:
            console.print("[yellow]Generation failed. Using manual entry.[/yellow]\n")
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

