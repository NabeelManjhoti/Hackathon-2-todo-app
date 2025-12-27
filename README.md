# Todo Application

A command-line todo application built with Python, following clean code principles and PEP 8 standards.

## Features

- Add new todo items
- Delete todo items
- Update todo items
- View all todo items
- Mark todo items as complete

## Requirements

- Python 3.13+
- UV package manager

## Project Structure

```
├── src/                 # Source code
│   ├── __init__.py
│   ├── main.py          # Main application entry point
│   ├── models/          # Data models
│   ├── cli/             # Command-line interface
│   └── services/        # Business logic
├── tests/               # Test files
├── specs/               # Feature specifications
├── .specify/            # Spec-driven development artifacts
├── history/             # History of prompts and decisions
├── CLAUDE.md            # Claude Code rules
├── README.md            # This file
└── pyproject.toml       # Project dependencies (if any)
```

## Getting Started

1. Install dependencies: `uv sync`
2. Run the application: `python -m src.main`

## Development

This project follows a spec-driven development approach. All changes should be documented in the appropriate spec files in the `specs/` directory.

## Constitution

This project follows the principles outlined in `.specify/memory/constitution.md`:
- Clean code following PEP 8 standards
- Modularity for easy maintenance and extension
- In-memory storage only (no persistence to files or databases)
- User-friendly command-line interface with clear instructions
- Error handling for invalid inputs 
