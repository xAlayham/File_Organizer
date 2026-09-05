# File Organiser

A Python command-line application that automatically organises files by renaming them and placing them into category-based folders.

## Features

* Batch file renaming
* Automatic file categorisation
* Duplicate file detection
* Operation preview before changes are made
* Dry-run mode
* Undo the most recent organisation operation
* Operation history stored in JSON
* Execution logging
* Configurable settings
* Command-line interface
* Automated test suite

## How It Works

File Organiser scans a folder and creates an operation plan for the files it finds.

For example:

```text
Before:

MyFolder/
├── photo.jpg
├── report.pdf
├── script.py
└── notes.txt
```

The organiser creates a plan and then renames and categorises the files:

```text
After:

MyFolder/
├── Image/
│   └── backup_1.jpg
├── Document/
│   ├── backup_2.pdf
│   └── backup_4.txt
└── Code/
    └── backup_3.py
```

Before making changes, the planned operations are displayed for review.

## Requirements

* Python 3.10 or newer
* No external Python packages are required.

The project uses only the Python standard library.

## Installation

Clone the repository:

```bash
git clone https://github.com/xAlayham/File_Organizer.git
cd file-organiser
```

No additional packages need to be installed.

## Usage

Run the application by providing the folder you want to organise:

```bash
python main.py <folder>
```

For example:

```bash
python main.py "C:\Users\Example\Downloads"
```

The application will scan the folder, categorise the files, display the planned operations, and ask for confirmation before making changes.

## Command-Line Options

### `--prefix`

Changes the prefix used when renaming files.

```bash
python main.py <folder> --prefix project
```

Example:

```text
photo.jpg → project_1.jpg
report.pdf → project_2.pdf
```

The default prefix is `backup`.

### `--dry-run`

Displays the planned operations without modifying any files.

```bash
python main.py <folder> --dry-run
```

This is useful for checking what the organiser would do before actually running it.

### `--no-confirm`

Skips the confirmation prompt and immediately executes the planned operations.

```bash
python main.py <folder> --no-confirm
```

### `--check-duplicates`

Checks the folder for duplicate files before the organisation process.

```bash
python main.py <folder> --check-duplicates
```

### `--undo`

Reverses the most recent organisation operation using the saved operation history.

```bash
python main.py <folder> --undo
```

After a successful undo, the saved history is cleared.

If there is no available history, the application reports:

```text
No undo history found
```

## Configuration

The application can optionally use a `config.json` file.

Example:

```json
{
    "default_prefix": "backup",
    "show_summary": true,
    "run_tests": true
}
```

If `config.json` is missing or contains malformed JSON, the application falls back to its default settings.

Settings provided in the configuration file are merged with the default settings.
* `default_prefix` — the prefix used when renaming files if `--prefix` isn't given.
* `show_summary` — when `true`, prints the file-count/category breakdown before renaming and the folder contents afterward.
* `run_tests` — when `true`, runs the automated test suite as a self-check before doing anything else, and aborts if any test fails.

## Logging

The application records execution information in log files.

Logs include:

* The folder that was organised
* The planned file operations
* The number of successful operations
* The number of failed operations
* Application start and completion information

## Undo System

Before an organisation operation is completed, the operations are saved to:

```text
.file_organiser_history.json
```

The history contains information about each file's original name, new name, and destination category.

When `--undo` is used, the application uses this information to move the files back to their original locations and names.

After a successful undo, the history file is removed.

## Duplicate Detection

The `--check-duplicates` option compares files and identifies files with identical content.

Example:

```bash
python main.py <folder> --check-duplicates
```

Duplicate files are displayed before the organisation process continues.

## Testing

The project includes an automated test suite using Python's built-in `unittest` framework.

Run all tests with:

```bash
python tests.py
```

The current test suite contains 51 tests covering the project's core functionality, including:

* Duplicate detection
* Undo operations
* History management
* Folder scanning
* File categorisation
* File renaming
* Operation planning
* File execution
* Command-line argument parsing
* Configuration loading
* Logging

The application has also been manually tested end-to-end using temporary test folders, including organisation, undo, and dry-run functionality.

## Project Structure

```text
file-organiser/
│
├── main.py
├── cli.py
├── config.py
├── scanner.py
├── categoriser.py
├── duplicates.py
├── renamer.py
├── planner.py
├── executor.py
├── undo.py
├── history.py
├── logger.py
├── display.py
├── system_logger.py
├── tests.py
│
└── README.md
```

### Module Overview

| Module             | Purpose                              |
| ------------------ | ------------------------------------ |
| `main.py`          | Coordinates the application          |
| `cli.py`           | Handles command-line arguments       |
| `config.py`        | Loads application configuration      |
| `scanner.py`       | Scans folders for files              |
| `categoriser.py`   | Determines file categories           |
| `duplicates.py`    | Detects duplicate files              |
| `renamer.py`       | Generates new file names             |
| `planner.py`       | Builds the organisation plan         |
| `executor.py`      | Renames and moves files              |
| `undo.py`          | Reverses organisation operations     |
| `history.py`       | Stores and manages operation history |
| `logger.py`        | Creates execution logs               |
| `display.py`       | Handles terminal output              |
| `system_logger.py` | Handles application logging          |
| `tests.py`         | Automated test suite                 |

## Current Status

The project is currently at **v1.0**.

Completed:

* [x] Project structure
* [x] Folder scanner
* [x] File categorisation
* [x] Duplicate detection
* [x] Operation planner
* [x] File renaming and moving
* [x] Undo system
* [x] Operation history
* [x] Logging
* [x] Command-line interface
* [x] Configuration file
* [x] Dry-run mode
* [x] Automated tests
* [x] End-to-end testing

## Future Improvements

Possible future improvements include:

* Support for more file categories and extensions
* More advanced configuration options
* Improved handling of name conflicts
* Optional cleanup of empty category folders
* More detailed summary reporting
* Additional automated integration tests

## License

This project is available for educational and personal use.
