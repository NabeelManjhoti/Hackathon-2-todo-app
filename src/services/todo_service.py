"""
Todo Application - Todo Service

This module contains the business logic for managing todo items.
"""
from typing import List
from models.todo import TodoItem


class TodoService:
    """Service class for managing todo items."""

    def __init__(self):
        """Initialize the todo service with an empty list of tasks."""
        self.tasks: List[TodoItem] = []

    def add_task(self, task: str) -> None:
        """
        Add a new task to the todo list.

        Args:
            task: The task description to add
        """
        new_task = TodoItem(task=task)
        self.tasks.append(new_task)

    def delete_task(self, index: int) -> None:
        """
        Delete a task at the specified index.

        Args:
            index: The index of the task to delete
        """
        if index < 0 or index >= len(self.tasks):
            raise IndexError(f"Task index {index} out of range")

        del self.tasks[index]

    def update_task(self, index: int, new_task: str) -> None:
        """
        Update a task at the specified index.

        Args:
            index: The index of the task to update
            new_task: The new task description
        """
        if index < 0 or index >= len(self.tasks):
            raise IndexError(f"Task index {index} out of range")

        if not new_task or not new_task.strip():
            raise ValueError("Task cannot be empty")

        self.tasks[index] = TodoItem(task=new_task, completed=self.tasks[index].completed)

    def get_tasks(self, completed_only: bool = False, pending_only: bool = False) -> List[TodoItem]:
        """
        Get tasks based on completion status.

        Args:
            completed_only: If True, return only completed tasks
            pending_only: If True, return only pending tasks

        Returns:
            List of tasks matching the criteria
        """
        if completed_only and pending_only:
            return []  # Can't be both completed and pending

        if completed_only:
            return [task for task in self.tasks if task.completed]

        if pending_only:
            return [task for task in self.tasks if not task.completed]

        return self.tasks

    def mark_complete(self, index: int) -> None:
        """
        Mark a task as complete.

        Args:
            index: The index of the task to mark complete
        """
        if index < 0 or index >= len(self.tasks):
            raise IndexError(f"Task index {index} out of range")

        self.tasks[index].completed = True