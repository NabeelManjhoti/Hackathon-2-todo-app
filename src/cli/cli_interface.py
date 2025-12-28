import argparse
from src.services.task_service import TaskService
from src.commands.command_handlers import CommandHandlers


class CLIInterface:
    """
    Command-line interface for the Todo application using argparse.
    """

    def __init__(self):
        """
        Initialize the CLI interface with task service and command handlers.
        """
        self.task_service = TaskService()
        self.command_handlers = CommandHandlers(self.task_service)
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create and configure the argument parser with all subcommands.

        Returns:
            argparse.ArgumentParser: Configured argument parser
        """
        parser = argparse.ArgumentParser(
            prog="todo",
            description="A command-line todo application",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        # Create subparsers for different commands
        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Add command: Add a new task
        add_parser = subparsers.add_parser("add", help="Add a new task")
        add_parser.add_argument("title", help="Title of the task")
        add_parser.add_argument("--description", "-d", default="", help="Description of the task")

        # List command: List all tasks
        list_parser = subparsers.add_parser("list", help="List all tasks")

        # Complete command: Mark a task as complete
        complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
        complete_parser.add_argument("id", type=int, help="ID of the task to mark as complete")

        # Incomplete command: Mark a task as incomplete
        incomplete_parser = subparsers.add_parser("incomplete", help="Mark a task as incomplete")
        incomplete_parser.add_argument("id", type=int, help="ID of the task to mark as incomplete")

        # Update command: Update a task's attributes
        update_parser = subparsers.add_parser("update", help="Update a task")
        update_parser.add_argument("id", type=int, help="ID of the task to update")
        update_parser.add_argument("--title", help="New title for the task")
        update_parser.add_argument("--description", "-d", help="New description for the task")

        # Delete command: Delete a task
        delete_parser = subparsers.add_parser("delete", help="Delete a task")
        delete_parser.add_argument("id", type=int, help="ID of the task to delete")

        return parser

    def run(self, args=None):
        """
        Run the CLI interface with the provided arguments.

        Args:
            args: Command-line arguments (if None, uses sys.argv)
        """
        parsed_args = self.parser.parse_args(args)

        # If no command was provided, show help
        if not parsed_args.command:
            self.parser.print_help()
            return

        # Route to appropriate handler based on command
        if parsed_args.command == "add":
            result = self.command_handlers.handle_add(parsed_args.title, parsed_args.description)
        elif parsed_args.command == "list":
            result = self.command_handlers.handle_list()
        elif parsed_args.command == "complete":
            result = self.command_handlers.handle_complete(parsed_args.id)
        elif parsed_args.command == "incomplete":
            result = self.command_handlers.handle_incomplete(parsed_args.id)
        elif parsed_args.command == "update":
            # Only pass values if they were explicitly provided
            title = parsed_args.title if hasattr(parsed_args, 'title') and parsed_args.title is not None else None
            description = parsed_args.description if hasattr(parsed_args, 'description') and parsed_args.description is not None else None
            result = self.command_handlers.handle_update(parsed_args.id, title, description)
        elif parsed_args.command == "delete":
            result = self.command_handlers.handle_delete(parsed_args.id)
        else:
            result = f"Unknown command: {parsed_args.command}"

        print(result)