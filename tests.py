import unittest
import tempfile
import os
from duplicates import find_duplicates

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

if __name__ == "__main__":
    unittest.main()