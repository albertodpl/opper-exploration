# Claude Code Configuration

This file contains configuration and context for Claude Code to help with project-specific tasks.

## Project Overview

<!-- Add a brief description of your project here -->

## Commands

<!-- Add commonly used commands for this project -->

### Development
```bash
# Run main.py (room extraction example)
source ./venv/bin/activate && source .env && python src/opperexploration/main.py

# Run task_completion.py (knowledge base query example)
source ./venv/bin/activate && source .env && python src/opperexploration/task_completion.py
```

### Testing
```bash
# Add your testing commands here
```

### Build
```bash
# Add your build commands here
```

### Linting
```bash
# Run ruff linter
source ./venv/bin/activate && ruff check src/

# Run ruff formatter
source ./venv/bin/activate && ruff format src/
```

## Project Structure

<!-- Describe the key directories and files in your project -->

## Notes

### Python Invocation
- Local Python: Use `python3` command
- Within venv: Use `python` command
- Always activate venv first: `source ./venv/bin/activate`

### Environment Variables
- Copy `.env.example` to `.env` and add your API keys
- Load environment variables: `source .env` or use python-dotenv
- `.env` file is gitignored to prevent committing secrets

### Git Commits
- Do not mention Claude Code or AI assistance in commit messages
- Keep commit messages professional and focused on the actual changes