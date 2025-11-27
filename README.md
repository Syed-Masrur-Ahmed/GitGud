# GitGud - AI-Powered Git Assistant

> An intelligent Python CLI that makes Git operations effortless with AI-powered recommendations

## Project Overview

GitGud is a Python command-line tool that uses AI (Ollama + CodeLlama) to analyze your Git repository state and recommend the optimal push strategy. No more failed pushes, confusing errors, or Git anxiety!

```bash
$ gitgud push

Analyzing repository...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Repository State
  Branch: feature/login
  Ahead:  3 commits
  Behind: 1 commit

AI Recommendation (confidence: 85%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Strategy: pull-then-push
Reasoning: Pull with rebase to maintain linear history

Commands:
  1. git pull --rebase origin feature/login
  2. git push origin feature/login

Execute? [Y/n]
```

## Features

### `gitgud status` - Repository Health Dashboard

Beautiful terminal UI showing your repository state at a glance:

```
╭─────────────────────────────────────────╮
│  Repository Health                      │
│  Repository  GitGud                     │
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

### `gitgud commit` - Smart Commit with AI Messages

**NEW!** Create commits with AI-generated messages:

- Analyzes your changes and generates appropriate commit messages
- Follows Conventional Commits format (feat, fix, docs, etc.)
- Interactive approval/edit workflow
- Fallback to heuristic generation if AI unavailable
- Option to use manual messages

**Example:**
```bash
$ gitgud commit --ai

GitGud Smart Commit

Changes to be committed:
  Modified:  3 files
  Untracked: 1 files

Generating commit message with AI...

Generated commit message:
┌────────────────────────────────────────┐
│ feat: add AI-powered commit messages   │
│                                        │
│ - Implement CommitMessageGenerator     │
│ - Add commit command with AI support   │
│ - Support manual and AI-generated msgs │
└────────────────────────────────────────┘

? What would you like to do?
  > Use this message
    Edit message
    Enter manually
    Cancel
```

### `gitgud push` - Smart Push with AI

Analyzes your repo and recommends the optimal push strategy:
- Handles ahead/behind scenarios
- Auto-stashes uncommitted changes
- Detects divergent branches
- AI + heuristic fallback
- Shows risks before executing

### `gitgud resolve` - Interactive Divergence Helper

**NEW!** Stuck with divergent branches? This command walks you through resolution:

- Explains what happened in plain English
- Shows your options (rebase, merge, force push)
- Pros/cons for each approach
- AI-powered recommendations
- Interactive step-by-step execution

**Example:**
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

## Documentation

- **[PYTHON_PRD.md](PYTHON_PRD.md)** - Complete product requirements and vision
- **[PYTHON_IMPLEMENTATION_PLAN.md](PYTHON_IMPLEMENTATION_PLAN.md)** - Step-by-step build guide

## Quick Start

### Installation (Development Mode)

```bash
# Clone and setup
git clone https://github.com/Syed-Masrur-Ahmed/GitGud.git
cd GitGud
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e .

# Setup AI (optional, first time)
ollama pull codellama:7b
```

### Usage

```bash
cd your-git-repo

# See repository health dashboard
gitgud status

# Commit with AI-generated message
gitgud commit --ai

# Commit with manual message
gitgud commit -m "your message"

# Smart push with AI analysis
gitgud push

# Resolve divergent branches interactively
gitgud resolve

# Use heuristics without AI
gitgud push --no-ai

# Get help
gitgud --help
```

## Build Timeline

- **Estimated Time:** 15-20 hours (11 hours core + buffer)
- **Difficulty:** Easy-Medium (2.5/5)
- **MVP Features:** Smart push, status dashboard, AI analysis

## Tech Stack

- **Language:** Python 3.9+
- **CLI Framework:** Click + Rich (beautiful terminal UI)
- **Git Integration:** GitPython
- **AI:** Ollama + CodeLlama (local, free, private)
- **Distribution:** PyPI + PyInstaller (single binary)

## Why Python Over Node.js?

- **Industry Standard** - Most Git/DevOps tools are Python (aws-cli, ansible)
- **Faster to build** - 15-20 hours vs 25+ for Node.js
- **Cleaner code** - Less boilerplate, more readable
- **Better libraries** - GitPython, Click, Rich are superior
- **Single binary** - PyInstaller creates standalone executables
- **Native AI ecosystem** - Python is the AI language

## Project Structure

```
gitgud/
├── README.md                           # This file
├── PYTHON_PRD.md                       # Product requirements
├── PYTHON_IMPLEMENTATION_PLAN.md       # Build guide (start here!)
└── archive/
    ├── vscode-extension/               # Old VS Code extension work
    │   ├── GitGud/                     # Extension code (archived)
    │   ├── PRD.md                      # Extension PRD (archived)
    │   └── IMPLEMENTATION_PLAN.md      # Extension plan (archived)
    └── nodejs-cli/                     # Old Node.js CLI work
        ├── CLI_PRD.md                  # Node.js PRD (archived)
        └── CLI_IMPLEMENTATION_PLAN.md  # Node.js plan (archived)
```

## Implementation Status

- [x] Phase 0: Environment Setup (Complete)
- [x] Phase 1: Project Initialization (Complete)
- [x] Phase 2: Git Integration (Complete)
- [x] Phase 3: AI Services (Complete)
- [x] Phase 4: Smart Push Command (Complete)
- [x] **BONUS: Resolve Command** (Complete) - Interactive divergent branch helper
- [x] Phase 5: Polish & Documentation (Complete)
- [ ] Phase 6: Publish to PyPI (Coming soon)

**Status: MVP Complete!**

## Learning Outcomes

Building this project teaches:
- Python CLI tool development (Click + Rich)
- Git internals and operations (GitPython)
- AI integration (Ollama/LLMs)
- Beautiful terminal UI design
- Python packaging (PyPI + PyInstaller)
- Open source project management

## Next Steps

1. **Read the PRD:** Open [PYTHON_PRD.md](PYTHON_PRD.md) to understand the vision
2. **Follow the plan:** Open [PYTHON_IMPLEMENTATION_PLAN.md](PYTHON_IMPLEMENTATION_PLAN.md)
3. **Start building:** Begin with Phase 0 (Environment Setup - 30 min)
4. **Ship it:** Publish to PyPI and share with the world!

## Future Enhancements

### Already Built
- Smart push/pull analysis
- Divergent branch resolution
- Beautiful Rich terminal UI
- AI + heuristic providers
- AI-generated commit messages (`gitgud commit`)

### Coming Next
- Smart pull command
- Deep repository analysis (`gitgud analyze`)
- Interactive TUI mode (like lazygit)
- VS Code extension wrapper (reuse CLI logic)
- Team collaboration insights
- Git hooks integration
- PyInstaller single binary distribution

## License

MIT (to be added)

## Author

Your Name - [GitHub](https://github.com/yourusername)

---

**Ready to make Git easy for everyone? Start building!**

Follow the Python implementation plan step-by-step, and you'll have a working CLI in 15-20 hours.

### Why Python Won:
- **40% faster to build** than Node.js version
- **Better libraries** - Click + Rich are best-in-class
- **Industry standard** - DevOps tools are Python
- **Easier distribution** - Single binary with PyInstaller

