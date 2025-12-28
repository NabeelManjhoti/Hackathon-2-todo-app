import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from src.cli.cli_interface import CLIInterface
from src.services.task_service import TaskService
from src.commands.command_handlers import CommandHandlers


class TestCLI(unittest.TestCase):
    """
    Test cases for the CLI functionality.
    """

    def setUp(self):
        """Set up a CLIInterface instance for each test."""
        self.cli = CLIInterface()

    def test_add_command_handler(self):
        """Test the add command handler."""
        result = self.cli.command_handlers.handle_add("Test Task", "Test Description")
        self.assertIn("Added task", result)
        self.assertIn("Test Task", result)

        # Verify the task was actually created
        tasks = self.cli.task_service.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Test Task")
        self.assertEqual(tasks[0].description, "Test Description")

    def test_list_command_handler_with_tasks(self):
        """Test the list command handler with tasks."""
        # Add some tasks first
        self.cli.task_service.create_task("Task 1", "Description 1")
        self.cli.task_service.create_task("Task 2", "Description 2")

        result = self.cli.command_handlers.handle_list()
        self.assertIn("Task 1", result)
        self.assertIn("Task 2", result)
        self.assertIn("O", result)  # Should show incomplete status

    def test_list_command_handler_empty(self):
        """Test the list command handler with no tasks."""
        result = self.cli.command_handlers.handle_list()
        self.assertEqual(result, "No tasks found.")

    def test_complete_command_handler(self):
        """Test the complete command handler."""
        task = self.cli.task_service.create_task("Test Task", "Description")
        self.assertFalse(task.completion_status)

        result = self.cli.command_handlers.handle_complete(task.id)
        self.assertIn("marked as complete", result)

        # Verify the task was updated
        updated_task = self.cli.task_service.get_task(task.id)
        self.assertTrue(updated_task.completion_status)

    def test_incomplete_command_handler(self):
        """Test the incomplete command handler."""
        task = self.cli.task_service.create_task("Test Task", "Description")
        completed_task = self.cli.task_service.complete_task(task.id)
        self.assertTrue(completed_task.completion_status)

        result = self.cli.command_handlers.handle_incomplete(task.id)
        self.assertIn("marked as incomplete", result)

        # Verify the task was updated
        updated_task = self.cli.task_service.get_task(task.id)
        self.assertFalse(updated_task.completion_status)

    def test_update_command_handler(self):
        """Test the update command handler."""
        task = self.cli.task_service.create_task("Original Title", "Original Description")

        result = self.cli.command_handlers.handle_update(task.id, title="New Title", description="New Description")
        self.assertIn("Updated task", result)

        # Verify the task was updated
        updated_task = self.cli.task_service.get_task(task.id)
        self.assertEqual(updated_task.title, "New Title")
        self.assertEqual(updated_task.description, "New Description")

    def test_update_command_handler_partial(self):
        """Test the update command handler with partial updates."""
        task = self.cli.task_service.create_task("Original Title", "Original Description")

        # Update only title
        result = self.cli.command_handlers.handle_update(task.id, title="New Title")
        self.assertIn("title to 'New Title'", result)

        updated_task = self.cli.task_service.get_task(task.id)
        self.assertEqual(updated_task.title, "New Title")
        self.assertEqual(updated_task.description, "Original Description")  # Should remain unchanged

    def test_delete_command_handler(self):
        """Test the delete command handler."""
        task = self.cli.task_service.create_task("Test Task", "Description")

        result = self.cli.command_handlers.handle_delete(task.id)
        self.assertIn("Deleted task", result)

        # Verify the task was deleted
        deleted_task = self.cli.task_service.get_task(task.id)
        self.assertIsNone(deleted_task)

    def test_error_handling_for_invalid_task_ids(self):
        """Test error handling for operations on non-existent task IDs."""
        # Test complete command with invalid ID
        result = self.cli.command_handlers.handle_complete(999)
        self.assertIn("Error:", result)
        self.assertIn("does not exist", result)

        # Test incomplete command with invalid ID
        result = self.cli.command_handlers.handle_incomplete(999)
        self.assertIn("Error:", result)
        self.assertIn("does not exist", result)

        # Test update command with invalid ID
        result = self.cli.command_handlers.handle_update(999, title="New Title")
        self.assertIn("Error:", result)
        self.assertIn("does not exist", result)

        # Test delete command with invalid ID
        result = self.cli.command_handlers.handle_delete(999)
        self.assertIn("Error:", result)
        self.assertIn("does not exist", result)

    def test_help_command_simulation(self):
        """Test that help information is available (simulated)."""
        # This tests that the parser was created with proper help text
        parser = self.cli._create_parser()
        help_text = parser.format_help()
        self.assertIn("add", help_text)
        self.assertIn("list", help_text)
        self.assertIn("complete", help_text)
        self.assertIn("incomplete", help_text)
        self.assertIn("update", help_text)
        self.assertIn("delete", help_text)


if __name__ == '__main__':
    unittest.main()