import click
import inquirer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from gitgud.services.git.git_service import GitService
from gitgud.services.git.context_builder import ContextBuilder
from gitgud.services.ai.ai_service import AIService

console = Console()

@click.command()
@click.option('-y', '--yes', is_flag=True, help='Skip confirmation prompts')
@click.option('--no-ai', is_flag=True, help='Use heuristics only (no AI)')
def push(yes, no_ai):
    """Smart push with AI analysis."""
    git = GitService()
    
    # Check if in git repo
    if not git.is_git_repository():
        console.print("[red]❌ Not in a git repository[/red]")
        raise click.Abort()
    
    console.print("\n[bold cyan]🚀 GitGud Smart Push[/bold cyan]\n")
    
    # Step 1: Build context
    with console.status("[bold green]Analyzing repository..."):
        context_builder = ContextBuilder(git)
        context = context_builder.build_context()
    
    if not context:
        console.print("[red]Failed to analyze repository[/red]")
        raise click.Abort()
    
    console.print("[green]✓[/green] Repository analyzed\n")
    
    # Display current state
    state_table = Table(show_header=False, box=None, padding=(0, 1))
    state_table.add_column("Label", style="dim")
    state_table.add_column("Value", style="white")
    state_table.add_row("📦 Branch:", context.local_branch)
    state_table.add_row("↑ Ahead:", f"[green]{context.commits_ahead}[/green] commits")
    state_table.add_row("↓ Behind:", f"[yellow]{context.commits_behind}[/yellow] commits")
    state_table.add_row("📝 Changes:", str(context.uncommitted_changes))
    
    console.print(state_table)
    console.print()
    
    # Step 2: Get AI recommendation
    with console.status("[bold blue]Getting AI recommendation..."):
        ai_service = AIService(provider_type="heuristic" if no_ai else "ollama")
        try:
            response = ai_service.analyze(context)
        except Exception as e:
            console.print(f"[red]AI analysis failed: {e}[/red]")
            raise click.Abort()
    
    console.print("[green]✓[/green] AI analysis complete\n")
    
    # Step 3: Display recommendation
    console.print(f"[bold cyan]🤖 AI Recommendation[/bold cyan] [dim](confidence: {response.confidence}%)[/dim]")
    console.print("━" * 50)
    console.print(f"[bold]Strategy:[/bold] {response.strategy}")
    console.print(f"[bold]Reasoning:[/bold] {response.reasoning}")
    
    # Handle manual review
    if response.requires_manual_review or not response.commands:
        console.print(f"\n[yellow]⚠️  Manual review required[/yellow]")
        console.print("[dim]This situation needs your attention.[/dim]\n")
        return
    
    # Display commands
    console.print(f"\n[bold]📝 Commands to execute:[/bold]")
    for idx, cmd in enumerate(response.commands, 1):
        console.print(f"  [dim]{idx}.[/dim] [cyan]{cmd}[/cyan]")
    
    # Display risks
    if response.risks:
        console.print(f"\n[bold yellow]⚠️  Potential risks:[/bold yellow]")
        for risk in response.risks:
            console.print(f"  [yellow]•[/yellow] {risk}")
    
    # Step 4: Get confirmation
    if not yes:
        console.print()
        questions = [
            inquirer.Confirm('execute',
                           message="Execute these commands?",
                           default=True),
        ]
        answers = inquirer.prompt(questions)
        
        if not answers or not answers['execute']:
            console.print("\n[dim]Operation cancelled[/dim]\n")
            return
    
    # Step 5: Execute commands
    console.print(f"\n[bold green]✨ Executing commands...[/bold green]\n")
    
    for cmd in response.commands:
        with console.status(f"[cyan]{cmd}[/cyan]"):
            success = git.execute_command(f"git {cmd.replace('git ', '')}")
        
        if success:
            console.print(f"[green]✓[/green] [dim]{cmd}[/dim]")
        else:
            console.print(f"[red]✗[/red] [red]{cmd} failed[/red]")
            console.print("\n[red]❌ Stopped execution due to error[/red]\n")
            raise click.Abort()
    
    console.print(f"\n[bold green]✅ Success![/bold green] All commands executed.\n")