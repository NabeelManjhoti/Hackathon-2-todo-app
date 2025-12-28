from src.models.task import Task
from typing import List, Optional


class TaskService:
    """
    Service layer for managing tasks with in-memory storage.
    """

    def __init__(self):
        """
        Initialize the TaskService with empty storage and next ID counter.
        """
        self._tasks = {}  # Dictionary for O(1) lookup with task ID as key
        self._next_id = 1  # Tracks next available ID starting from 1

    def create_task(self, title: str, description: str = "") -> Task:
        """
        Create a new task with auto-generated ID.

        Args:
            title (str): Title of the task
            description (str): Optional description of the task

        Returns:
            Task: The created Task instance

        Raises:
            ValueError: If title is empty
        """
        if not title or title.strip() == "":
            raise ValueError("Task title cannot be empty")

        task_id = self._next_id
        self._next_id += 1

        task = Task(id=task_id, title=title.strip(), description=description.strip())
        self._tasks[task_id] = task

        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id (int): ID of the task to retrieve

        Returns:
            Task: The task with the given ID, or None if not found
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks.

        Returns:
            List[Task]: List of all tasks
        """
        return list(self._tasks.values())

    def update_task(self, task_id: int, title: str = None, description: str = None,
                   completion_status: bool = None) -> Optional[Task]:
        """
        Update an existing task's attributes.

        Args:
            task_id (int): ID of the task to update
            title (str, optional): New title for the task
            description (str, optional): New description for the task
            completion_status (bool, optional): New completion status for the task

        Returns:
            Task: The updated task, or None if task doesn't exist

        Raises:
            ValueError: If task doesn't exist or if title is empty when provided
        """
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} does not exist")

        task = self._tasks[task_id]

        if title is not None:
            if not title or title.strip() == "":
                raise ValueError("Task title cannot be empty")
            task.title = title.strip()

        if description is not None:
            task.description = description.strip()

        if completion_status is not None:
            task.completion_status = completion_status

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id (int): ID of the task to delete

        Returns:
            bool: True if task was deleted, False if task didn't exist

        Raises:
            ValueError: If task doesn't exist
        """
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} does not exist")

        del self._tasks[task_id]
        return True

    def complete_task(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as complete.

        Args:
            task_id (int): ID of the task to mark as complete

        Returns:
            Task: The updated task, or None if task doesn't exist

        Raises:
            ValueError: If task doesn't exist
        """
        return self.update_task(task_id, completion_status=True)

    def incomplete_task(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as incomplete.

        Args:
            task_id (int): ID of the task to mark as incomplete

        Returns:
            Task: The updated task, or None if task doesn't exist

        Raises:
            ValueError: If task doesn't exist
        """
        return self.update_task(task_id, completion_status=False)