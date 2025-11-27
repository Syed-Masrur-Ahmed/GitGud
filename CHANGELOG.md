# Changelog

All notable changes to GitGud will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-27

### Added - MVP Release! 🎉

#### Commands
- **`gitgud status`** - Beautiful repository health dashboard
  - Shows branch, remote, commits ahead/behind, file changes
  - Color-coded health indicators (🟢 Clean, 🟡 Needs attention, 🔴 Divergent)
  - Helpful suggestions for next steps
  
- **`gitgud push`** - Smart push with AI/heuristic analysis
  - Analyzes repository state and recommends optimal strategy
  - Handles common scenarios (pull first, stash changes, etc.)
  - AI-powered with Ollama + rule-based heuristic fallback
  - Safety confirmations before execution
  - Shows risks and reasoning
  
- **`gitgud resolve`** - Interactive divergent branch resolver
  - Explains divergence situations in plain English
  - Shows all options (rebase, merge, force push) with pros/cons
  - AI-powered recommendations
  - Step-by-step guided execution
  - Handles uncommitted changes automatically

#### Core Services
- **Git Integration** via GitPython
  - Repository state analysis
  - Ahead/behind calculations
  - Branch tracking detection
  - Command execution
  
- **AI Services**
  - Ollama provider for AI-powered recommendations
  - Heuristic provider for rule-based decisions
  - Automatic fallback system for reliability
  - Context building from repository state

#### Infrastructure
- Click-based CLI with beautiful Rich terminal output
- Interactive prompts with inquirer
- Type-safe dataclasses for Git and AI types
- Comprehensive error handling
- Edge case handling (no remote, detached HEAD, etc.)

### Technical Details
- **Language**: Python 3.9+
- **Dependencies**: Click, Rich, GitPython, requests, PyYAML, inquirer
- **AI Model**: Ollama + CodeLlama (optional)
- **Distribution**: pip installable in development mode

### Documentation
- Comprehensive README with examples
- Detailed implementation plan
- Product requirements document
- Inline help text for all commands

## [Unreleased]

### Planned Features
- AI-generated commit messages
- Smart pull command
- Deep repository analysis
- PyPI package distribution
- PyInstaller single binary
- Basic test coverage
- VS Code extension integration

