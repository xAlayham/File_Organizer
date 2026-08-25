import unittest
import tempfile
import os
from duplicates import find_duplicates
from undo import undo_operation, undo_operations
import history

class TestFindDuplicates(unittest.TestCase):
    def test_find_duplicates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "a.txt"), "w") as file:
                file.write("Hello")

            with open(os.path.join(tmpdir, "b.txt"), "w") as file:
                file.write("Hello")

            with open(os.path.join(tmpdir, "c.txt"), "w") as file:
                file.write("Hello")

            duplicates = find_duplicates(tmpdir)
            result = []
            for key, value in duplicates.items():
                result.append(key)
                result.extend(value)
            duplicates = set(result)

            expected = ["a.txt", "b.txt", "c.txt"]
            expected = set(expected)

            self.assertEqual(duplicates, expected)

    def test_all_unique_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "a.txt"), "w") as file:
                file.write("Hello")
        
            with open(os.path.join(tmpdir, "b.txt"), "w") as file:
                file.write("Hell")

            with open(os.path.join(tmpdir, "c.txt"), "w") as file:
                file.write("Hel")

            duplicates = find_duplicates(tmpdir)

            self.assertEqual(duplicates, {})

    def test_empty_folder(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            duplicates = find_duplicates(tmpdir)

            self.assertEqual(duplicates, {})

class TestUndo(unittest.TestCase):
    def test_undo_operation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = os.path.join(tmpdir, "Images")
            os.mkdir(destination)

            organised_file = os.path.join(destination, "backup_1.jpg")

            with open(organised_file, "w") as file:
                file.write("test")

            operation = {
                "old": "photo.jpg",
                "new": "backup_1.jpg",
                "destination": "Images" 
            }

            result = undo_operation(tmpdir, operation)

            self.assertTrue(result)
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "photo.jpg")))
            self.assertFalse(os.path.exists(organised_file))

    def test_undo_multiple_operations(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            images = os.path.join(tmpdir, "Images")
            documents = os.path.join(tmpdir, "Documents")

            os.mkdir(images)
            os.mkdir(documents)

            image_file = os.path.join(images, "backup_1.jpg")
            document_file = os.path.join(documents, "backup_2.txt")

            with open(image_file, "w") as file:
                file.write("image")

            with open(document_file, "w") as file:
                file.write("document")

            operations = [
                {
                    "old": "photo.jpg",
                    "new": "backup_1.jpg",
                    "destination": "Images"
                },
                {
                    "old": "notes.txt",
                    "new": "backup_2.txt",
                    "destination": "Documents"
                }
            ]

            result = undo_operations(tmpdir, operations)

            self.assertEqual(result, 2)
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "photo.jpg")))
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "notes.txt")))
            self.assertFalse(os.path.exists(image_file))
            self.assertFalse(os.path.exists(document_file))

    def test_undo_missing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            os.mkdir(os.path.join(tmpdir, "Images"))

            operation = {
                "old": "photo.jpg",
                "new": "backup_1.jpg",
                "destination": "Images"
            }

            result = undo_operation(tmpdir, operation)

            self.assertFalse(result)

class TestHistory(unittest.TestCase):

    def test_save_and_load_history(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            operations = [
                {
                    "old": "photo.jpg",
                    "new": "backup_1.jpg",
                    "destination": "Images"
                },
                {
                    "old": "notes.txt",
                    "new": "backup_2.txt",
                    "destination": "Documents"
                }
            ]

            history.save_history(tmpdir, operations)

            loaded_operations = history.load_history(tmpdir)

            self.assertEqual(loaded_operations, operations)

    def test_load_missing_history(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = history.load_history(tmpdir)

            self.assertIsNone(result)

    def test_clear_history(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            operations = [
                {
                    "old": "photo.jpg",
                    "new": "backup_1.jpg",
                    "destination": "Images"
                }
            ]

            history.save_history(tmpdir, operations)

            history.clear_history(tmpdir)

            result = history.load_history(tmpdir)

            self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()