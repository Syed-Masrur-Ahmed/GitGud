# GitGud CLI (Python) - Product Requirements Document

## 1. Executive Summary

**Product Name:** GitGud  
**Type:** Python Command-Line Interface (CLI) Tool  
**Version:** 1.0.0  
**Language:** Python 3.9+  
**Last Updated:** November 14, 2025

### 1.1 Vision Statement
GitGud is an intelligent Python CLI that eliminates Git complexity using AI. Analyze repository state, get AI recommendations, and execute optimal Git strategies—all from your terminal.

### 1.2 Why Python?
- ✅ **Industry Standard**: Most DevOps/Git tools are Python (aws-cli, ansible, etc.)
- ✅ **Better Git Libraries**: GitPython is mature and powerful
- ✅ **Cleaner Code**: More readable, less boilerplate than JavaScript
- ✅ **Rich CLI Ecosystem**: Click + Rich = beautiful, powerful CLIs
- ✅ **Single Binary Distribution**: Package as standalone executable with PyInstaller
- ✅ **Faster Development**: Estimated 15-20 hours vs 25+ for Node.js
- ✅ **Better AI Integration**: Native Python AI/ML ecosystem

### 1.3 Product Goals
- Replace `git push` with `gitgud push` for intelligent automation
- Reduce Git errors by 90%
- Install in < 30 seconds: `pip install gitgud-cli`
- Work with any editor (Vim, VS Code, IntelliJ, etc.)
- Use free local AI (Ollama + CodeLlama)
- Package as single binary (no Python installation required)

---

## 2. Core Features

### 2.1 Smart Push (MVP)

#### Command
```bash
gitgud push
```

#### Output
```bash
$ gitgud push

🔍 Analyzing repository...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Repository State
  Branch: feature/login
  ↑ Ahead:  3 commits
  ↓ Behind: 1 commit
  📝 Changes: 2 modified files

🤖 AI Recommendation (confidence: 85%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Strategy: pull-then-push
Reasoning: Remote has new commits. Pull with 
          rebase to maintain linear history.

📝 Commands to execute:
  1. git pull --rebase origin feature/login
  2. git push origin feature/login

⚠️  Potential risks:
  • Rebase may cause conflicts

Execute these commands? [Y/n]: █
```

### 2.2 Repository Status

#### Command
```bash
gitgud status
```

#### Output with Rich Table
```bash
$ gitgud status

╭─────────────────────────────────────────╮
│  Repository Health Dashboard            │
├─────────────────────────────────────────┤
│                                         │
│  📦 Repository: my-awesome-app          │
│  🌿 Branch:     feature/new-login       │
│  🔗 Remote:     origin/main             │
│                                         │
│  Status: 🟡 NEEDS SYNC                  │
│                                         │
│  ┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓  │
│  ┃ Metric      ┃ Value              ┃  │
│  ┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩  │
│  │ Ahead       │ 3 commits          │  │
│  │ Behind      │ 1 commit           │  │
│  │ Modified    │ 2 files            │  │
│  │ Untracked   │ 0 files            │  │
│  │ Stashed     │ 1 stash            │  │
│  └─────────────┴────────────────────┘  │
│                                         │
│  💡 Run 'gitgud push' to sync           │
│                                         │
╰─────────────────────────────────────────╯
```

### 2.3 Deep Analysis

#### Command
```bash
gitgud analyze
```

#### Features
- Comprehensive repository health check
- AI insights on branch state
- Recommendations for next steps
- Potential issue detection (large files, secrets, etc.)

### 2.4 Smart Pull

#### Command
```bash
gitgud pull
```

#### Features
- Auto-stashes uncommitted changes
- Chooses rebase vs merge intelligently
- Handles simple conflicts with AI
- Provides conflict resolution guidance

### 2.5 AI Commit Messages

#### Command
```bash
gitgud commit           # AI generates message
gitgud commit -m "msg"  # Manual message
```

#### Example
```bash
$ git add .
$ gitgud commit

🤖 Analyzing staged changes...

Suggested commit message:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
feat: Add user authentication with JWT

- Implement login endpoint with password validation
- Add bcrypt for secure password hashing  
- Create JWT token generation and validation
- Add authentication middleware for protected routes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Use this message? [Y/n/edit]: █
```

### 2.6 Configuration

#### Command
```bash
gitgud config           # Interactive setup
gitgud config list      # Show settings
gitgud config set key value
```

#### Config File Location
- **Linux/Mac**: `~/.config/gitgud/config.yaml`
- **Windows**: `%APPDATA%\gitgud\config.yaml`

---

## 3. Technical Architecture

### 3.1 Technology Stack

#### Core Framework
- **Language**: Python 3.9+
- **CLI Framework**: Click 8.x (command routing) + Rich 13.x (beautiful output)
- **Git Integration**: GitPython 3.x
- **HTTP Client**: requests 2.x (for Ollama API)
- **Config**: PyYAML 6.x
- **Packaging**: PyInstaller 6.x (single binary)

#### Why These Choices?

**Click over Typer:**
- More mature, battle-tested (used by Flask, AWS CLI)
- Simpler for our use case
- Better documentation

**Rich over alternatives:**
- Best-in-class terminal output
- Tables, progress bars, panels, syntax highlighting
- Active development

**GitPython over subprocess:**
- Pythonic API
- Better error handling
- Type hints

### 3.2 Project Structure

```
gitgud/
├── gitgud/
│   ├── __init__.py
│   ├── __main__.py              # Entry point
│   ├── cli.py                   # CLI setup (Click)
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── push.py              # gitgud push
│   │   ├── pull.py              # gitgud pull
│   │   ├── status.py            # gitgud status
│   │   ├── analyze.py           # gitgud analyze
│   │   ├── commit.py            # gitgud commit
│   │   └── config.py            # gitgud config
│   ├── services/
│   │   ├── __init__.py
│   │   ├── git/
│   │   │   ├── __init__.py
│   │   │   ├── git_service.py   # Git operations
│   │   │   ├── state_scanner.py # Repository analysis
│   │   │   └── context_builder.py
│   │   ├── ai/
│   │   │   ├── __init__.py
│   │   │   ├── ai_service.py    # AI orchestrator
│   │   │   ├── ollama.py        # Ollama provider
│   │   │   └── heuristic.py     # Rule-based fallback
│   │   └── safety/
│   │       ├── __init__.py
│   │       └── validator.py     # Safety checks
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── display.py           # Rich formatting
│   │   └── prompts.py           # User input
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py            # Config management
│   │   ├── logger.py            # Logging
│   │   └── errors.py            # Error handling
│   └── types/
│       ├── __init__.py
│       ├── git_types.py         # Git type hints
│       └── ai_types.py          # AI type hints
├── tests/
│   ├── __init__.py
│   ├── test_git.py
│   ├── test_ai.py
│   └── test_commands.py
├── setup.py                     # Package setup
├── pyproject.toml               # Modern Python packaging
├── requirements.txt             # Dependencies
├── requirements-dev.txt         # Dev dependencies
├── README.md
├── LICENSE
└── .gitignore
```

### 3.3 Installation Methods

#### Method 1: pip (Recommended for Users)
```bash
pip install gitgud-cli
```

#### Method 2: pipx (Isolated environment)
```bash
pipx install gitgud-cli
```

#### Method 3: Single Binary (No Python needed!)
```bash
# Download from GitHub releases
curl -L https://github.com/user/gitgud/releases/download/v1.0.0/gitgud-macos -o gitgud
chmod +x gitgud
mv gitgud /usr/local/bin/
```

#### Method 4: From Source (Developers)
```bash
git clone https://github.com/user/gitgud-cli
cd gitgud-cli
pip install -e .
```

### 3.4 Dependencies

#### Core (requirements.txt)
```txt
click>=8.1.0
rich>=13.0.0
GitPython>=3.1.0
requests>=2.31.0
PyYAML>=6.0
inquirer>=3.1.0
```

#### Development (requirements-dev.txt)
```txt
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.0.0
mypy>=1.5.0
flake8>=6.1.0
pre-commit>=3.3.0
```

---

## 4. AI Integration

### 4.1 Ollama Provider (Primary)

#### Python Implementation
```python
import requests
import json

class OllamaProvider:
    def __init__(self, endpoint="http://localhost:11434", model="codellama:7b"):
        self.endpoint = endpoint
        self.model = model
    
    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.endpoint}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def analyze(self, context: dict) -> dict:
        prompt = self._build_prompt(context)
        
        response = requests.post(
            f"{self.endpoint}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            },
            timeout=30
        )
        
        result = response.json()
        return json.loads(result["response"])
```

### 4.2 Alternative: ollama-python Package

```python
from ollama import Client

client = Client(host='http://localhost:11434')
response = client.generate(
    model='codellama:7b',
    prompt=prompt,
    format='json'
)
```

---

## 5. User Experience

### 5.1 Command Structure

```bash
gitgud [OPTIONS] COMMAND [ARGS]

Commands:
  push       Smart push with AI analysis
  pull       Smart pull with conflict handling  
  status     Repository health dashboard
  analyze    Deep repository analysis
  commit     Smart commit (optional AI messages)
  config     Configuration management
  init       First-time setup wizard

Options:
  -h, --help       Show help message
  -v, --version    Show version
  -y, --yes        Skip confirmations (auto-yes)
  --no-ai          Disable AI (use heuristics only)
  --verbose        Show detailed output
  --dry-run        Show what would happen
  --debug          Show debug information
```

### 5.2 Rich Terminal Output

Python's `rich` library provides:
- ✅ **Progress bars** with spinners
- ✅ **Syntax highlighting** for diffs
- ✅ **Tables** for structured data
- ✅ **Panels** for grouped information
- ✅ **Live updates** for real-time feedback
- ✅ **Markdown rendering** in terminal
- ✅ **Tree views** for file structures

Example:
```python
from rich.console import Console
from rich.table import Table

console = Console()

table = Table(title="Repository Status")
table.add_column("Metric", style="cyan")
table.add_column("Value", style="green")
table.add_row("Ahead", "3 commits")
table.add_row("Behind", "1 commit")

console.print(table)
```

### 5.3 Interactive Prompts

Using `inquirer` for beautiful prompts:
```python
import inquirer

questions = [
    inquirer.Confirm('execute',
                     message="Execute these commands?",
                     default=True),
]

answers = inquirer.prompt(questions)
```

---

## 6. Packaging & Distribution

### 6.1 PyPI Package

#### setup.py
```python
from setuptools import setup, find_packages

setup(
    name="gitgud-cli",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.1.0",
        "rich>=13.0.0",
        "GitPython>=3.1.0",
        "requests>=2.31.0",
        "PyYAML>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "gitgud=gitgud.cli:main",
        ],
    },
    python_requires=">=3.9",
)
```

#### Publishing
```bash
python -m build
twine upload dist/*
```

### 6.2 Single Binary with PyInstaller

#### Build Script
```bash
pyinstaller --onefile \
            --name gitgud \
            --add-data "gitgud/templates:templates" \
            gitgud/cli.py
```

#### Benefits
- ✅ No Python installation needed
- ✅ Single executable file
- ✅ Faster startup time
- ✅ Easier distribution

#### Build for Multiple Platforms
```bash
# macOS
pyinstaller --onefile --target-arch x86_64 gitgud/cli.py

# Linux
docker run -v "$(pwd):/src" python:3.9 \
    bash -c "cd /src && pip install pyinstaller && pyinstaller --onefile gitgud/cli.py"

# Windows (on Windows machine)
pyinstaller --onefile gitgud\cli.py
```

---

## 7. Development Workflow

### 7.1 Setting Up Development Environment

```bash
# Clone repo
git clone https://github.com/user/gitgud-cli
cd gitgud-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in editable mode
pip install -e .
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Format code
black gitgud/
```

### 7.2 Code Quality Tools

#### Black (Formatting)
```bash
black gitgud/ tests/
```

#### MyPy (Type Checking)
```bash
mypy gitgud/
```

#### Flake8 (Linting)
```bash
flake8 gitgud/
```

#### pytest (Testing)
```bash
pytest tests/ -v --cov=gitgud
```

### 7.3 Pre-commit Configuration

`.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
  
  - repo: https://github.com/PyCQA/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.0
    hooks:
      - id: mypy
```

---

## 8. Testing Strategy

### 8.1 Unit Tests

```python
# tests/test_heuristic.py
import pytest
from gitgud.services.ai.heuristic import HeuristicProvider

def test_clean_push():
    provider = HeuristicProvider()
    context = {
        "commits_ahead": 3,
        "commits_behind": 0,
        "uncommitted_changes": 0,
        "is_divergent": False
    }
    
    result = provider.analyze(context)
    
    assert result["strategy"] == "push"
    assert "git push" in result["commands"]
    assert result["confidence"] > 90
```

### 8.2 Integration Tests

```python
# tests/test_git_service.py
from gitgud.services.git.git_service import GitService

def test_git_status(tmp_path):
    # Create a test git repo
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()
    
    # Initialize git
    import git
    repo = git.Repo.init(repo_path)
    
    # Test GitService
    service = GitService(str(repo_path))
    status = service.get_status()
    
    assert status is not None
    assert status["is_clean"] == True
```

### 8.3 CLI Tests

```python
# tests/test_cli.py
from click.testing import CliRunner
from gitgud.cli import cli

def test_version():
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
    assert '1.0.0' in result.output

def test_status_no_repo():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['status'])
        assert result.exit_code == 1
        assert 'not a git repository' in result.output.lower()
```

---

## 9. Performance Considerations

### 9.1 Startup Time

**Python CLI Optimization:**
- Lazy imports (only import when needed)
- Compiled .pyc files (Python automatically creates these)
- PyInstaller binary (faster startup, no import overhead)

```python
# Good: Lazy import
def push_command():
    from gitgud.services.ai import AIService  # Import only when used
    ai = AIService()

# Bad: Eager import at top
from gitgud.services.ai import AIService  # Slows down ALL commands
```

### 9.2 Target Performance

- **Cold start**: < 200ms (PyInstaller binary)
- **Analysis time**: < 3 seconds
- **AI response**: < 5 seconds (Ollama)
- **Memory**: < 50MB

---

## 10. Advantages Over Node.js Version

| Aspect | Python | Node.js |
|--------|--------|---------|
| **Code Length** | Shorter | Longer |
| **Dependencies** | Fewer | More packages |
| **Build Time** | **15-20 hours** | 25 hours |
| **Learning Curve** | Easier | Harder |
| **CLI Libraries** | Rich, Click (best) | Commander, Chalk (good) |
| **Git Library** | GitPython (mature) | simple-git (good) |
| **Single Binary** | ✅ Easy (PyInstaller) | ⚠️ Harder (pkg) |
| **Industry Standard** | ✅ DevOps norm | Web tooling |
| **AI Integration** | ✅ Native ecosystem | Good but external |
| **Type Safety** | Type hints + mypy | TypeScript (if used) |

---

## 11. Success Metrics

### 11.1 Adoption
- **Target**: 1,000 PyPI downloads in first month
- **Target**: 100+ GitHub stars in first month
- **Target**: Featured on Python Weekly

### 11.2 Quality
- **Target**: 4.5+ star rating on PyPI
- **Target**: 95% test coverage
- **Target**: 95% correct AI recommendations

---

## 12. Roadmap

### Phase 1: MVP (15-20 hours)
- ✅ CLI framework with Click
- ✅ Git integration with GitPython
- ✅ AI service (Ollama + heuristics)
- ✅ Smart push command
- ✅ Status command
- ✅ Beautiful Rich output
- ✅ PyPI package

### Phase 2: Enhanced (1 week)
- Smart pull
- AI commit messages
- Conflict resolution helper
- Configuration management

### Phase 3: Distribution (1 week)
- PyInstaller binaries (macOS, Linux, Windows)
- Homebrew formula
- Debian/Ubuntu package

---

## 13. Why Python Wins for This Project

### 13.1 Code Comparison

**Simple Git Status - Python:**
```python
# 15 lines, very readable
from git import Repo
from rich.console import Console

console = Console()
repo = Repo('.')
status = repo.git.status()

console.print(f"[green]Branch:[/green] {repo.active_branch}")
console.print(f"[yellow]Status:[/yellow] {status}")
```

**Same in Node.js:**
```javascript
// 25+ lines, more boilerplate
const simpleGit = require('simple-git');
const chalk = require('chalk');

const git = simpleGit();

git.status((err, status) => {
    if (err) {
        console.error(chalk.red('Error:'), err);
        process.exit(1);
    }
    
    console.log(chalk.green('Branch:'), status.current);
    console.log(chalk.yellow('Status:'), status);
});
```

### 13.2 Rich Terminal Output Comparison

**Python (Rich library):**
```python
from rich.console import Console
from rich.table import Table

console = Console()
table = Table(title="Repo Status")
table.add_column("Metric")
table.add_column("Value")
table.add_row("Ahead", "3")
console.print(table)
```

**Node.js (cli-table3):**
```javascript
const Table = require('cli-table3');
const chalk = require('chalk');

const table = new Table({
    head: ['Metric', 'Value'],
    colWidths: [20, 20]
});
table.push(['Ahead', '3']);
console.log(chalk.bold('Repo Status'));
console.log(table.toString());
```

**Python is cleaner, more intuitive, and produces better output!**

---

## 14. Next Steps

1. **Read Implementation Plan** - See PYTHON_IMPLEMENTATION_PLAN.md
2. **Start Building** - Begin with Phase 0 (setup)
3. **Iterate Quickly** - Python's simplicity = faster iteration
4. **Package & Ship** - PyPI + single binaries

---

**Document End**

*Python CLI optimized for speed, simplicity, and industry standards.*

