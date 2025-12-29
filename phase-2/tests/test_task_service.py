import unittest
from src.services.task_service import TaskService
from src.models.task import Task


class TestTaskService(unittest.TestCase):
    """
    Test cases for the TaskService.
    """

    def setUp(self):
        """Set up a fresh TaskService instance for each test."""
        self.service = TaskService()

    def test_create_task_with_auto_generated_id(self):
        """Test that create_task adds new task with auto-generated ID."""
        task = self.service.create_task("Test Title", "Test Description")

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Title")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.completion_status, False)

    def test_store_and_retrieve_task_by_id(self):
        """Test that tasks can be stored and retrieved by ID."""
        task = self.service.create_task("Test Title", "Test Description")
        retrieved_task = self.service.get_task(task.id)

        self.assertEqual(task.id, retrieved_task.id)
        self.assertEqual(task.title, retrieved_task.title)
        self.assertEqual(task.description, retrieved_task.description)
        self.assertEqual(task.completion_status, retrieved_task.completion_status)

    def test_auto_incrementing_id_generation(self):
        """Test that auto-incrementing ID generation works correctly."""
        task1 = self.service.create_task("Task 1")
        task2 = self.service.create_task("Task 2")
        task3 = self.service.create_task("Task 3")

        self.assertEqual(task1.id, 1)
        self.assertEqual(task2.id, 2)
        self.assertEqual(task3.id, 3)

    def test_get_all_tasks(self):
        """Test that get_all_tasks returns all tasks."""
        task1 = self.service.create_task("Task 1")
        task2 = self.service.create_task("Task 2")
        task3 = self.service.create_task("Task 3")

        all_tasks = self.service.get_all_tasks()

        self.assertEqual(len(all_tasks), 3)
        self.assertIn(task1, all_tasks)
        self.assertIn(task2, all_tasks)
        self.assertIn(task3, all_tasks)

    def test_update_task_title_and_description(self):
        """Test that update_task modifies task attributes correctly."""
        task = self.service.create_task("Original Title", "Original Description")

        updated_task = self.service.update_task(task.id, title="New Title", description="New Description")

        self.assertEqual(updated_task.title, "New Title")
        self.assertEqual(updated_task.description, "New Description")

    def test_update_task_partial(self):
        """Test that partial updates work correctly."""
        task = self.service.create_task("Original Title", "Original Description")

        # Only update the title
        updated_task = self.service.update_task(task.id, title="New Title")

        self.assertEqual(updated_task.title, "New Title")
        self.assertEqual(updated_task.description, "Original Description")  # Should remain unchanged

        # Only update the description
        updated_task2 = self.service.update_task(task.id, description="New Description")

        self.assertEqual(updated_task2.title, "New Title")  # Should remain unchanged
        self.assertEqual(updated_task2.description, "New Description")

    def test_delete_task_by_id(self):
        """Test that delete_task removes task by ID."""
        task = self.service.create_task("Test Title")
        result = self.service.delete_task(task.id)

        self.assertTrue(result)
        self.assertIsNone(self.service.get_task(task.id))

    def test_operations_on_non_existent_ids(self):
        """Test operations on non-existent IDs handle gracefully."""
        # Try to get a non-existent task
        non_existent_task = self.service.get_task(999)
        self.assertIsNone(non_existent_task)

        # Try to update a non-existent task
        with self.assertRaises(ValueError):
            self.service.update_task(999, title="New Title")

        # Try to delete a non-existent task
        with self.assertRaises(ValueError):
            self.service.delete_task(999)

        # Try to complete a non-existent task
        with self.assertRaises(ValueError):
            self.service.complete_task(999)

        # Try to mark incomplete a non-existent task
        with self.assertRaises(ValueError):
            self.service.incomplete_task(999)

    def test_prevent_empty_title_on_creation(self):
        """Test that prevents creation of tasks with empty titles."""
        with self.assertRaises(ValueError):
            self.service.create_task("")

        with self.assertRaises(ValueError):
            self.service.create_task("   ")  # Title with only spaces

        with self.assertRaises(ValueError):
            self.service.create_task(None)  # This would be caught by type checking

    def test_prevent_empty_title_on_update(self):
        """Test that prevents updating tasks with empty titles."""
        task = self.service.create_task("Valid Title")

        with self.assertRaises(ValueError):
            self.service.update_task(task.id, title="")

        with self.assertRaises(ValueError):
            self.service.update_task(task.id, title="   ")  # Title with only spaces

    def test_complete_task(self):
        """Test that complete_task marks task as complete."""
        task = self.service.create_task("Test Title")
        self.assertFalse(task.completion_status)

        completed_task = self.service.complete_task(task.id)
        self.assertTrue(completed_task.completion_status)

    def test_incomplete_task(self):
        """Test that incomplete_task marks task as incomplete."""
        task = self.service.create_task("Test Title")
        completed_task = self.service.complete_task(task.id)
        self.assertTrue(completed_task.completion_status)

        incomplete_task = self.service.incomplete_task(task.id)
        self.assertFalse(incomplete_task.completion_status)


if __name__ == '__main__':
    unittest.main()