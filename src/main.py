"""
Todo Application - Main Entry Point

This module serves as the entry point for the command-line todo application.
"""
import sys
import os
from pathlib import Path

# Add the src directory to the path so imports work correctly
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from cli.app import TodoApp


def main():
    """Main entry point for the todo application."""
    app = TodoApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()