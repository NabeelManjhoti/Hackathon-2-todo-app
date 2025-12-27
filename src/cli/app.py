"""
Todo Application - CLI Interface

This module contains the command-line interface for the todo application.
"""
import argparse
import sys
from services.todo_service import TodoService


class TodoApp:
    """Main application class for the todo CLI."""

    def __init__(self):
        """Initialize the todo application."""
        self.todo_service = TodoService()
        self.parser = self._create_parser()

    def _create_parser(self):
        """Create the argument parser with all available commands."""
        parser = argparse.ArgumentParser(
            description="A simple command-line todo application"
        )
        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Add command
        add_parser = subparsers.add_parser("add", help="Add a new todo item")
        add_parser.add_argument("task", help="The task to add")

        # Delete command
        delete_parser = subparsers.add_parser("delete", help="Delete a todo item")
        delete_parser.add_argument("index", type=int, help="Index of the task to delete")

        # Update command
        update_parser = subparsers.add_parser("update", help="Update a todo item")
        update_parser.add_argument("index", type=int, help="Index of the task to update")
        update_parser.add_argument("task", help="The updated task")

        # List command
        list_parser = subparsers.add_parser("list", help="List all todo items")
        list_parser.add_argument("--completed", action="store_true", help="Show only completed tasks")
        list_parser.add_argument("--pending", action="store_true", help="Show only pending tasks")

        # Complete command
        complete_parser = subparsers.add_parser("complete", help="Mark a todo as complete")
        complete_parser.add_argument("index", type=int, help="Index of the task to mark complete")

        return parser

    def run(self):
        """Run the application with the provided arguments."""
        if len(sys.argv) == 1:
            self.parser.print_help()
            return

        args = self.parser.parse_args()

        try:
            if args.command == "add":
                self.todo_service.add_task(args.task)
                print(f"Added task: {args.task}")
            elif args.command == "delete":
                self.todo_service.delete_task(args.index)
                print(f"Deleted task at index {args.index}")
            elif args.command == "update":
                self.todo_service.update_task(args.index, args.task)
                print(f"Updated task at index {args.index} to: {args.task}")
            elif args.command == "list":
                tasks = self.todo_service.get_tasks(
                    completed_only=args.completed,
                    pending_only=args.pending
                )
                if tasks:
                    for i, task in enumerate(tasks):
                        status = "X" if task.completed else "O"
                        print(f"{i}. [{status}] {task.task}")
                else:
                    print("No tasks found.")
            elif args.command == "complete":
                self.todo_service.mark_complete(args.index)
                print(f"Marked task at index {args.index} as complete")
            else:
                self.parser.print_help()
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except IndexError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)