import unittest
from src.models.task import Task


class TestTask(unittest.TestCase):
    """
    Test cases for the Task model.
    """

    def test_task_creation_with_attributes(self):
        """Test that Task can be instantiated with all required attributes."""
        task = Task(id=1, title="Test Task", description="Test Description", completion_status=False)

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.completion_status, False)

    def test_task_default_completion_status(self):
        """Test that new tasks have completion_status set to False by default."""
        task = Task(id=1, title="Test Task", description="Test Description")

        self.assertEqual(task.completion_status, False)

    def test_task_string_representation(self):
        """Test that Task string representation includes all attributes."""
        task = Task(id=1, title="Test Task", description="Test Description", completion_status=True)
        expected = "[X] 1: Test Task - Test Description"

        self.assertEqual(str(task), expected)

    def test_task_string_representation_incomplete(self):
        """Test that Task string representation shows incomplete status correctly."""
        task = Task(id=1, title="Test Task", description="Test Description", completion_status=False)
        expected = "[O] 1: Test Task - Test Description"

        self.assertEqual(str(task), expected)

    def test_task_repr(self):
        """Test the developer-friendly representation of Task."""
        task = Task(id=1, title="Test Task", description="Test Description", completion_status=True)
        expected = "Task(id=1, title='Test Task', description='Test Description', completion_status=True)"

        self.assertEqual(repr(task), expected)


if __name__ == '__main__':
    unittest.main()