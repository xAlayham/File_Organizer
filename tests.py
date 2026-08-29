import unittest
import tempfile
import os
from duplicates import find_duplicates
from undo import undo_operation, undo_operations
import history
from scanner import scan_folder, scan_folder_recursive
from categoriser import file_category, categorise_files, count_categories
from renamer import rename_files
from planner import build_operations
from executor import execute_rename, execute_plan, create_folder, move_file
from cli import parse_args
from config import load_config
from logger import get_timestamp, create_log_file, write_execution_log

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

    def test_undo_operations_removes_empty_destination_folders(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            image_folder = os.path.join(tmpdir, "Image")
            document_folder = os.path.join(tmpdir, "Document")

            os.makedirs(image_folder)
            os.makedirs(document_folder)

            with open(os.path.join(image_folder, "backup_1.jpg"), "w") as file:
                file.write("image")

            with open(os.path.join(document_folder, "backup_2.pdf"), "w") as file:
                file.write("document")

            operations = [
                {
                    "old": "photo.jpg",
                    "new": "backup_1.jpg",
                    "destination": "Image"
                },
                {
                    "old": "report.pdf",
                    "new": "backup_2.pdf",
                    "destination": "Document"
                }
            ]

            result = undo_operations(tmpdir, operations)

            self.assertEqual(result, 2)

            self.assertTrue(
                os.path.exists(os.path.join(tmpdir, "photo.jpg"))
            )

            self.assertTrue(
                os.path.exists(os.path.join(tmpdir, "report.pdf"))
            )

            self.assertFalse(os.path.exists(image_folder))
            self.assertFalse(os.path.exists(document_folder))

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

class TestScanner(unittest.TestCase):

    def test_scan_folder(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "a.txt"), "w") as file:
                file.write("Hello")

            with open(os.path.join(tmpdir, "b.txt"), "w") as file:
                file.write("World")

            result = scan_folder(tmpdir)

            self.assertEqual(set(result), {"a.txt", "b.txt"})

    def test_scan_empty_folder(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = scan_folder(tmpdir)

            self.assertEqual(result, [])

    def test_scan_missing_folder(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            missing_folder = os.path.join(tmpdir, "does_not_exist")

            result = scan_folder(missing_folder)

            self.assertIsNone(result)

    def test_scan_ignores_dictionaries(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            os.mkdir(os.path.join(tmpdir, "Images"))

            with open(os.path.join(tmpdir, "photo.jpg"), "w") as file:
                file.write("test")

            result = scan_folder(tmpdir)

            self.assertEqual(result, ["photo.jpg"])

    def test_scan_ignores_history_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, ".file_organiser_history.json"), "w") as file:
                file.write("[]")

            with open(os.path.join(tmpdir, "photo.jpg"), "w") as file:
                file.write("test")

            result = scan_folder(tmpdir)

            self.assertEqual(result, ["photo.jpg"])

    def test_scan_folder_recursive(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            images = os.path.join(tmpdir, "Images")
            documents = os.path.join(tmpdir, "Documents")

            os.mkdir(images)
            os.mkdir(documents)

            image_file = os.path.join(images, "photo.jpg")
            document_file = os.path.join(documents, "notes.txt")

            with open(image_file, "w") as file:
                file.write("image")

            with open(document_file, "w") as file:
                file.write("notes")

            result = scan_folder_recursive(tmpdir)

            self.assertEqual(
                set(result),
                {image_file, document_file}
            )

class TestCategoriser(unittest.TestCase):

    def test_file_category_image(self):
        self.assertEqual(file_category("photo.jpg"), "Image")
        self.assertEqual(file_category("picture.png"), "Image")

    def test_file_category_document(self):
        self.assertEqual(file_category("report.pdf"), "Document")
        self.assertEqual(file_category("notes.txt"), "Document")

    def test_file_category_code_and_other(self):
        self.assertEqual(file_category("script.py"), "Code")
        self.assertEqual(file_category("program.exe"), "Other")

    def test_file_category_case_insensitive(self):
        self.assertEqual(file_category("PHOTO.JPG"), "Image")
        self.assertEqual(file_category("REPORT.PDF"), "Document")
        self.assertEqual(file_category("SCRIPT.PY"), "Code")

    def test_categorise_files(self):
        files = [
            "photo.jpg",
            "report.pdf",
            "script.py",
            "notes.txt",
            "program.exe"
        ]

        result = categorise_files(files)

        expected = {
            "Image": ["photo.jpg"],
            "Document": ["report.pdf", "notes.txt"],
            "Code": ["script.py"],
            "Other": ["program.exe"]
        }

        self.assertEqual(result, expected)

    def test_count_categories(self):
        categories = {
            "Image": ["a.jpg", "b.png"],
            "Document": ["report.pdf"],
            "Code": ["script.py", "test.py", "main.py"]
        }

        result = count_categories(categories)

        expected = {
            "Image": 2,
            "Document": 1,
            "Code": 3
        }

        self.assertEqual(result, expected)

class TestRenamer(unittest.TestCase):

    def test_rename_file(self):
        result = rename_files("photo.jpg", 1, "backup")

        self.assertEqual(result, "backup_1.jpg")

    def test_rename_different_extension(self):
        result = rename_files("report.pdf", 5, "file")

        self.assertEqual(result, "file_5.pdf")

    def test_rename_prefix_and_number(self):
        result = rename_files("notes.txt", 42, "document")

        self.assertEqual(result, "document_42.txt")

    def test_rename_file_without_extension(self):
        result = rename_files("README", 3, "backup")

        self.assertEqual(result, "backup_3")

    def test_rename_uppercase_extension(self):
        result = rename_files("PHOTO.JPG", 2, "backup")

        self.assertEqual(result, "backup_2.JPG")

class TestPlanner(unittest.TestCase):

    def test_build_operations(self):
        files = ["photo.jpg"]

        result = build_operations(files, "backup")

        expected = [
            {
                "old": "photo.jpg",
                "new": "backup_1.jpg",
                "destination": "Image"
            }
        ]

        self.assertEqual(result, expected)

    def test_build_operations_multiple_files(self):
        files = [
            "photo.jpg",
            "report.pdf",
            "script.py"
        ]

        result = build_operations(files, "backup")

        expected = [
            {
                "old": "photo.jpg",
                "new": "backup_1.jpg",
                "destination": "Image"
            },
            {
                "old": "report.pdf",
                "new": "backup_2.pdf",
                "destination": "Document"
            },
            {
                "old": "script.py",
                "new": "backup_3.py",
                "destination": "Code"
            }
        ]

        self.assertEqual(result, expected)

    def test_build_operations_empty(self):
        result = build_operations([], "backup")

        self.assertEqual(result, [])

    def test_build_operations_custom_prefix(self):
        files = ["photo.jpg", "notes.txt"]

        result = build_operations(files, "project")

        expected = [
            {
                "old": "photo.jpg",
                "new": "project_1.jpg",
                "destination": "Image"
            },
            {
                "old": "notes.txt",
                "new": "project_2.txt",
                "destination": "Document"
            }
        ]

        self.assertEqual(result, expected)

class TestExecutor(unittest.TestCase):

    def test_execute_rename(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            old_path = os.path.join(tmpdir, "photo.jpg")

            with open(old_path, "w") as file:
                file.write("test")

            result = execute_rename(
                tmpdir,
                "photo.jpg",
                "backup_1.jpg"
            )

            self.assertTrue(result)
            self.assertFalse(os.path.exists(old_path))
            self.assertTrue(
                os.path.exists(os.path.join(tmpdir, "backup_1.jpg"))
            )

    def test_execute_rename_missing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = execute_rename(
                   tmpdir,
                "does_not_exist.txt",
                "backup_1.txt"
            )

            self.assertFalse(result)

    def test_create_folder(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            create_folder(tmpdir, "Images")

            destination = os.path.join(tmpdir, "Images")

            self.assertTrue(os.path.isdir(destination))

    def test_create_existing_folder(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            create_folder(tmpdir, "Images")
            create_folder(tmpdir, "Images")

            destination = os.path.join(tmpdir, "Images")

            self.assertTrue(os.path.isdir(destination))

    def test_move_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            create_folder(tmpdir, "Images")

            file_path = os.path.join(tmpdir, "photo.jpg")

            with open(file_path, "w") as file:
                file.write("test")

            move_file(tmpdir, "Images", "photo.jpg")

            self.assertFalse(os.path.exists(file_path))

            moved_path = os.path.join(
                tmpdir,
                "Images",
                "photo.jpg"
            )

            self.assertTrue(os.path.exists(moved_path))

    def test_execute_plan(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "photo.jpg"), "w") as file:
                file.write("image")

            with open(os.path.join(tmpdir, "notes.txt"), "w") as file:
                file.write("notes")

            operations = [
                {
                    "old": "photo.jpg",
                    "new": "backup_1.jpg",
                    "destination": "Image"
                },
                {
                    "old": "notes.txt",
                    "new": "backup_2.txt",
                    "destination": "Document"
                }
            ]

            result = execute_plan(tmpdir, operations)

            self.assertEqual(result["renamed"], 2)
            self.assertEqual(result["failed"], 0)

            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        tmpdir,
                        "Image",
                        "backup_1.jpg"
                    )
                )
            )

            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        tmpdir,
                        "Document",
                        "backup_2.txt"
                    )
                )
            )

    def test_execute_plan_with_failure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            operations = [
                {
                    "old": "missing.jpg",
                    "new": "backup_1.jpg",
                    "destination": "Image"
                }
            ]

            result = execute_plan(tmpdir, operations)

            self.assertEqual(result["renamed"], 0)
            self.assertEqual(result["failed"], 1)

class TestCLI(unittest.TestCase):

    def test_folder_argument(self):
        import sys

        old_argv = sys.argv

        try:
            sys.argv = ["main.py", "test_folder"]

            args = parse_args()

            self.assertEqual(args.folder, "test_folder")

        finally:
            sys.argv = old_argv

    def test_default_prefix(self):
        import sys

        old_argv = sys.argv

        try:
            sys.argv = ["main.py", "test_folder"]

            args = parse_args()

            self.assertEqual(args.prefix, "backup")

        finally:
            sys.argv = old_argv

    def test_custom_prefix(self):
        import sys

        old_argv = sys.argv

        try:
            sys.argv = [
                "main.py",
                "test_folder",
                "--prefix",
                "project"
            ]

            args = parse_args()

            self.assertEqual(args.prefix, "project")

        finally:
            sys.argv = old_argv

    def test_boolean_flags(self):
        import sys

        old_argv = sys.argv

        try:
            sys.argv = [
                "main.py",
                "test_folder",
                "--dry-run",
                "--no-confirm",
                "--check-duplicates",
                "--undo"
            ]

            args = parse_args()

            self.assertTrue(args.dry_run)
            self.assertTrue(args.no_confirm)
            self.assertTrue(args.check_duplicates)
            self.assertTrue(args.undo)

        finally:
            sys.argv = old_argv

    def test_boolean_flags_default_false(self):
        import sys

        old_argv = sys.argv

        try:
            sys.argv = ["main.py", "test_folder"]

            args = parse_args()

            self.assertFalse(args.dry_run)
            self.assertFalse(args.no_confirm)
            self.assertFalse(args.check_duplicates)
            self.assertFalse(args.undo)

        finally:
            sys.argv = old_argv

class TestConfig(unittest.TestCase):

    def test_load_valid_config(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, "config.json")

            with open(config_path, "w") as file:
                file.write('{"default_prefix": "project", "show_summary": false}')

            result = load_config(config_path)

            self.assertEqual(result["default_prefix"], "project")
            self.assertFalse(result["show_summary"])
            self.assertTrue(result["run_tests"])

    def test_missing_config_uses_defaults(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, "does_not_exist.json")
            result = load_config(config_path)

            self.assertEqual(
                result,
                {
                    "default_prefix": "backup",
                    "show_summary": True,
                    "run_tests": True
                }
            )

    def test_malformed_config_uses_defaults(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, "config.json")

            with open(config_path, "w") as file:
                file.write('{"default_prefix": "backup",')

            result = load_config(config_path)

            self.assertEqual(
                result,
                {
                    "default_prefix": "backup",
                    "show_summary": True,
                    "run_tests": True
                }
            )

    def test_config_merges_with_defaults(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, "config.json")

            with open(config_path, "w") as file:
                file.write('{"default_prefix": "test"}')

            result = load_config(config_path)

            self.assertEqual(result["default_prefix"], "test")
            self.assertTrue(result["show_summary"])
            self.assertTrue(result["run_tests"])

class TestLogger(unittest.TestCase):

    def test_get_timestamp(self):
        result = get_timestamp()

        self.assertRegex(
            result,
            r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$"
        )

    def test_create_log_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            old_directory = os.getcwd()

            try:
                os.chdir(tmpdir)

                result = create_log_file()

                self.assertTrue(result.startswith("logs"))
                self.assertTrue(result.endswith(".log"))
                self.assertTrue(os.path.isdir("logs"))

            finally:
                os.chdir(old_directory)

    def test_write_execution_log(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = os.path.join(tmpdir, "test.log")

            operations = [
                {
                    "old": "photo.jpg",
                    "new": "backup_1.jpg",
                    "destination": "Image"
                },
                {
                    "old": "notes.txt",
                    "new": "backup_2.txt",
                    "destination": "Document"
                }
            ]

            result = {
                "renamed": 2,
                "failed": 0
            }

            write_execution_log(
                log_path,
                tmpdir,
                operations,
                result
            )

            self.assertTrue(os.path.exists(log_path))

            with open(log_path, "r") as file:
                contents = file.read()

            self.assertIn("Application started", contents)
            self.assertIn(f"Folder: {tmpdir}", contents)
            self.assertIn(
                "photo.jpg -> backup_1.jpg (Image)",
                contents
            )
            self.assertIn(
                "notes.txt -> backup_2.txt (Document)",
                contents
            )
            self.assertIn("Renamed: 2", contents)
            self.assertIn("Failed: 0", contents)
            self.assertIn("Application Finished", contents)

    def test_write_execution_log_with_failure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = os.path.join(tmpdir, "test.log")

            operations = [
                {
                    "old": "missing.jpg",
                    "new": "backup_1.jpg",
                    "destination": "Image"
                }
            ]

            result = {
                "renamed": 0,
                "failed": 1
            }

            write_execution_log(
                log_path,
                tmpdir,
                operations,
                result
            )

            with open(log_path, "r") as file:
                contents = file.read()

            self.assertIn("Renamed: 0", contents)
            self.assertIn("Failed: 1", contents)

if __name__ == "__main__":
    unittest.main()
