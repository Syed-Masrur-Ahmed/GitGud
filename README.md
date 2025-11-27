# GitGud - AI-Powered Git Assistant

> Make Git operations effortless with intelligent analysis and recommendations

GitGud is a command-line tool that analyzes your Git repository and provides smart recommendations for push, pull, and commit operations. No more failed pushes, confusing errors, or Git anxiety!

## Features

### Repository Health Dashboard

See your repository state at a glance with a beautiful terminal UI:

```bash
$ gitgud status

╭─────────────────────────────────────────╮
│  Repository Health                      │
│  Repository  my-project                 │
│  Branch      main                       │
│  Remote      origin/main                │
│                                         │
│  Status      [OK] CLEAN                 │
│                                         │
│  Commits                                │
│    Ahead      0 commits                 │
│    Behind     0 commits                 │
│                                         │
│  Changes                                │
│    Modified     0 files                 │
│    Untracked    0 files                 │
╰─────────────────────────────────────────╯
```

### Smart Commit Messages

Automatically generate descriptive commit messages from your changes:

```bash
$ gitgud commit

GitGud Smart Commit

Changes to be committed:
  Modified:  3 files
  Untracked: 1 files

Generating commit message...

Generated commit message:
┌────────────────────────────────────────┐
│ feat: add user authentication          │
│                                        │
│ - add auth service                     │
│ - add login component                  │
│ - update routes                        │
└────────────────────────────────────────┘

? What would you like to do?
  > Use this message
    Edit message
    Enter manually
    Cancel
```

**Features:**
- Analyzes file changes and diff patterns
- Follows Conventional Commits format (feat, fix, docs, etc.)
- Interactive approval and editing
- Optional AI enhancement with `--ai` flag

### Smart Push

Intelligent push strategy based on repository state:

```bash
$ gitgud push

Analyzing repository...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Repository State
  Branch: feature/login
  Ahead:  3 commits
  Behind: 1 commit

Recommendation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Strategy: pull-then-push
Reasoning: Pull with rebase to maintain linear history

Commands:
  1. git pull --rebase origin feature/login
  2. git push origin feature/login

Execute? [Y/n]
```

**Handles:**
- Ahead/behind scenarios
- Uncommitted changes (auto-stash)
- Divergent branches
- Untracked remote branches

### Divergent Branch Resolution

Interactive guidance when your branch has diverged:

```bash
$ gitgud resolve

Branch Divergence Detected

Your situation:
├─ You have 2 local commits
└─ Remote has 3 commits you don't have

Your Options:
1. Pull --rebase (RECOMMENDED)
   + Clean history, linear timeline
   - May cause conflicts

2. Pull (merge)
   + Safe & simple
   - Creates merge commit

3. Force push (DANGEROUS)
   ! DELETES teammate's work

Recommendation: git pull --rebase
? How would you like to resolve this? (Use arrows)
  > Pull with rebase (keeps history clean)
    Pull with merge (safer)
    Cancel
```

## Installation

### From PyPI (Recommended)

```bash
pip install gitgud-cli
```

### From Source

```bash
git clone https://github.com/Syed-Masrur-Ahmed/GitGud.git
cd GitGud
pip install -e .
```

### Optional: AI Enhancement

For experimental AI-powered features, install Ollama:

```bash
# Install Ollama (https://ollama.ai)
ollama pull codellama:7b
```

AI features are optional - GitGud works great with smart heuristics alone.

## Usage

```bash
# Navigate to any Git repository
cd your-git-repo

# Check repository health
gitgud status

# Commit with auto-generated message
gitgud commit

# Commit with AI enhancement (experimental)
gitgud commit --ai

# Commit with manual message
gitgud commit -m "your message"

# Smart push
gitgud push

# Resolve divergent branches
gitgud resolve

# Show help
gitgud --help
```

## Commands

| Command | Description |
|---------|-------------|
| `gitgud status` | Show repository health dashboard |
| `gitgud commit` | Create commit with smart message generation |
| `gitgud push` | Intelligent push with analysis |
| `gitgud resolve` | Interactive divergent branch helper |

## Tech Stack

- **Python 3.9+**
- **Click** - CLI framework
- **Rich** - Beautiful terminal output
- **GitPython** - Git integration
- **Ollama** - Optional AI enhancement (local, private)

## How It Works

GitGud analyzes your repository using:

1. **Git state inspection** - branches, commits, changes
2. **Pattern recognition** - detects common scenarios
3. **Smart heuristics** - rule-based recommendations
4. **Optional AI** - LLM-powered insights (experimental)

All analysis happens locally. No data is sent to external services.

## Configuration

GitGud works out of the box with sensible defaults. No configuration needed.

For AI features, ensure Ollama is running:
```bash
ollama serve
```

## Contributing

Contributions welcome! Please feel free to submit issues and pull requests.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Author

**Syed Masrur Ahmed**
- GitHub: [@Syed-Masrur-Ahmed](https://github.com/Syed-Masrur-Ahmed)
- Email: ahmedsyedmasrur@gmail.com

---

**Make Git effortless. Install GitGud today!**

```bash
pip install gitgud-cli
```
