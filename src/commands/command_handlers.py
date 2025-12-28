from src.services.task_service import TaskService
from typing import Optional


class CommandHandlers:
    """
    Handles individual CLI commands by calling appropriate service methods.
    """

    def __init__(self, task_service: TaskService):
        """
        Initialize command handlers with a task service instance.

        Args:
            task_service (TaskService): Instance of the task service
        """
        self.task_service = task_service

    def handle_add(self, title: str, description: str = "") -> str:
        """
        Handle the 'add' command to create a new task.

        Args:
            title (str): Title of the task to add
            description (str): Optional description of the task

        Returns:
            str: Success message with task details
        """
        try:
            task = self.task_service.create_task(title, description)
            return f"Added task #{task.id}: {task.title}"
        except ValueError as e:
            return f"Error: {str(e)}"

    def handle_list(self) -> str:
        """
        Handle the 'list' command to display all tasks.

        Returns:
            str: Formatted list of all tasks or message if no tasks exist
        """
        tasks = self.task_service.get_all_tasks()

        if not tasks:
            return "No tasks found."

        # Sort tasks by ID for consistent display
        sorted_tasks = sorted(tasks, key=lambda t: t.id)

        task_list = []
        for task in sorted_tasks:
            status = "X" if task.completion_status else "O"
            task_list.append(f"[{status}] {task.id}: {task.title} - {task.description}")

        return "\n".join(task_list)

    def handle_complete(self, task_id: int) -> str:
        """
        Handle the 'complete' command to mark a task as complete.

        Args:
            task_id (int): ID of the task to mark as complete

        Returns:
            str: Success or error message
        """
        try:
            task = self.task_service.complete_task(task_id)
            return f"Task #{task.id} marked as complete: {task.title}"
        except ValueError as e:
            return f"Error: {str(e)}"

    def handle_incomplete(self, task_id: int) -> str:
        """
        Handle the 'incomplete' command to mark a task as incomplete.

        Args:
            task_id (int): ID of the task to mark as incomplete

        Returns:
            str: Success or error message
        """
        try:
            task = self.task_service.incomplete_task(task_id)
            return f"Task #{task.id} marked as incomplete: {task.title}"
        except ValueError as e:
            return f"Error: {str(e)}"

    def handle_update(self, task_id: int, title: str = None, description: str = None) -> str:
        """
        Handle the 'update' command to modify a task's attributes.

        Args:
            task_id (int): ID of the task to update
            title (str, optional): New title for the task
            description (str, optional): New description for the task

        Returns:
            str: Success or error message
        """
        try:
            # Only update fields that are explicitly provided
            updated_task = self.task_service.update_task(
                task_id,
                title=title if title is not None else None,
                description=description if description is not None else None
            )

            changes = []
            if title is not None:
                changes.append(f"title to '{updated_task.title}'")
            if description is not None:
                changes.append(f"description to '{updated_task.description}'")

            return f"Updated task #{updated_task.id}: {', '.join(changes)}"
        except ValueError as e:
            return f"Error: {str(e)}"

    def handle_delete(self, task_id: int) -> str:
        """
        Handle the 'delete' command to remove a task.

        Args:
            task_id (int): ID of the task to delete

        Returns:
            str: Success or error message
        """
        try:
            self.task_service.delete_task(task_id)
            return f"Deleted task #{task_id}"
        except ValueError as e:
            return f"Error: {str(e)}"