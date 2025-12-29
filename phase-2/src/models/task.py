class Task:
    """
    Represents a task with id, title, description, and completion status.
    """

    def __init__(self, id, title, description="", completion_status=False):
        """
        Initialize a Task instance.

        Args:
            id (int): Unique identifier for the task
            title (str): Title of the task
            description (str): Optional description of the task
            completion_status (bool): Whether the task is completed (default: False)
        """
        self.id = id
        self.title = title
        self.description = description
        self.completion_status = completion_status

    def __str__(self):
        """
        String representation of the task for debugging/display.

        Returns:
            str: Formatted string representation of the task
        """
        status = "X" if self.completion_status else "O"
        return f"[{status}] {self.id}: {self.title} - {self.description}"

    def __repr__(self):
        """
        Developer-friendly representation of the task.

        Returns:
            str: Representation showing all attributes
        """
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', completion_status={self.completion_status})"