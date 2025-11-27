# Changelog

All notable changes to GitGud will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.5] - 2025-11-27

### Fixed
- Fixed untracked file count bug in commit message generator
  - `_get_diff()` now only includes top-level untracked items
  - Prevents commit messages from trying to list thousands of files
  - Commit message generation now accurate for projects with large untracked directories

## [1.0.4] - 2025-11-27

### Fixed
- **Critical:** Fixed untracked file count bug in git status
  - Fixed in `git_service.py`: Status now shows correct untracked count
  - Previously: `frontend/` with 11,758 files reported as 11,758 untracked files
  - Now: `frontend/` correctly counted as 1 untracked directory

## [1.0.3] - 2025-11-27

### Fixed
- Improved heuristic commit message generation accuracy
- Removed overly specific keyword matching that caused false positives
- Added warning when committing >100 files at once
- More conservative and generic for large changesets

### Changed
- Heuristic now prioritizes actual code changes over generic keywords
- Better handling of large file counts

## [1.0.2] - 2025-11-27

### Fixed
- Fixed packaging issue: added missing `__init__.py` to `types` module
- Package now installs and imports correctly

## [1.0.1] - 2025-11-27

### Changed
- Improved README documentation with cleaner, user-focused content
- Removed internal development documentation from repository
- Enhanced CHANGELOG formatting
- Updated package metadata

## [1.0.0] - 2025-11-27

### Added

#### Core Commands
- **`gitgud status`** - Repository health dashboard
  - Real-time branch and remote status
  - Commits ahead/behind tracking
  - File changes overview
  - Color-coded health indicators
  - Actionable next-step suggestions
  
- **`gitgud commit`** - Smart commit message generation
  - Automatic message generation from changes
  - Conventional Commits format support (feat, fix, docs, etc.)
  - Interactive editing and approval
  - Pattern detection (features, fixes, refactoring)
  - Optional AI enhancement with `--ai` flag
  - Fast heuristic-based default mode
  
- **`gitgud push`** - Intelligent push analysis
  - Context-aware strategy recommendations
  - Automatic scenario detection (ahead, behind, divergent)
  - Safety confirmations with risk assessment
  - Uncommitted changes handling
  - AI and heuristic-based analysis
  
- **`gitgud resolve`** - Divergent branch resolution
  - Clear explanation of divergence situations
  - Interactive option selection (rebase, merge, force push)
  - Pros and cons for each approach
  - Guided step-by-step execution
  - Automatic stashing of uncommitted changes

#### Technical Features
- Click-based CLI framework with Rich terminal output
- GitPython integration for repository operations
- Optional Ollama AI provider with automatic fallback
- Rule-based heuristic provider for reliability
- Type-safe dataclasses for Git and AI contexts
- Comprehensive error handling and edge cases
- Interactive prompts with inquirer

### Technical Details
- **Python**: 3.9+ required
- **Core Dependencies**: Click, Rich, GitPython, inquirer
- **Optional Dependencies**: Ollama for AI features
- **License**: MIT

### Distribution
- Available via pip in development mode
- PyPI package: `gitgud-cli`

## [Unreleased]

### Planned Features
- Smart pull command with conflict detection
- Deep repository analysis and insights
- Single binary distribution via PyInstaller
- Test coverage and CI/CD
- Performance optimizations

---

For installation and usage instructions, see [README.md](README.md)
