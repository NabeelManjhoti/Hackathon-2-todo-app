#!/usr/bin/env python3
"""
Main entry point for the Todo application.
"""

import sys
from src.cli.cli_interface import CLIInterface


def main():
    """
    Main function to run the Todo application.
    """
    try:
        cli = CLIInterface()
        cli.run()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()