def print_operations(operations: list[dict]) -> None:
    """Display the planned file operations."""

    total = len(operations)

    print_heading("OPERATION REVIEW")

    for i, operation in enumerate(operations, start=1):
        print(f"[{i}/{total}]")
        print(f"Old: {operation['old']}")
        print(f"New: {operation['new']}")
        print(f"Destination: {operation['destination']}")
        print()


def print_heading(heading: str) -> None:
    """Display a formatted section heading."""

    print(f"\n=== {heading} ===\n")


def confirm_action(prompt: str, auto_confirm: bool = False) -> bool:
    """Ask the user to confirm an action."""

    if auto_confirm:
        return True

    return input(f"{prompt} (y/n): ").lower() == "y"


def print_categories(categories: dict[str, list[str]]) -> None:
    """Display files grouped by category."""

    for category, filenames in categories.items():
        print(f"{category} ({len(filenames)}) {' '.join(filenames)}")


def print_files(files: list[str]) -> None:
    """Display a list of files."""

    for file in files:
        print(file)


def print_progress(current: int, total: int, filename: str) -> None:
    """Display progress for a file operation."""

    print(f"[{current}/{total}] {filename}")


def print_error(message: str) -> None:
    """Display an error message."""

    print(f"ERROR: {message}")


def print_welcome() -> None:
    """Display the application welcome message."""

    print("=============\n")
    print("Batch File Organizer v1.0\n")
    print("=============\n")


def print_log_saved(log_path: str) -> None:
    """Display the location of the saved log file."""

    print(f"Log saved to: {log_path}")


def print_file_count(count: int) -> None:
    """Display the number of files found."""

    print(f"Found: {count} files")


def print_execution_report(result: dict) -> None:
    """Display the results of the file operations."""

    print("=== EXECUTION REPORT ===\n")
    print(f"Files renamed: {result['renamed']}")
    print(f"Failed: {result['failed']}")


def print_duplicates(duplicates: dict[str, list[str]]) -> None:
    """Display groups of duplicate files."""

    for key, value in duplicates.items():
        dupe_count = len(value)
        print(
            f"Found {dupe_count} duplicate(s) of "
            f"{duplicates[key]}: {', '.join(value)}"
        )


def print_undo_result(undone: int) -> None:
    """Display the number of successfully undone operations."""

    print(f"Undone {undone} operations")
