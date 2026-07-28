def print_operations(operations):
    total = len(operations)
    print_heading("OPERATION REVIEW")
    for i, operation in enumerate(operations, start=1):
        print(f"[{i}/{total}]")
        print(f"Old: {operation['old']}")
        print(f"New: {operation['new']}")
        print(f"Destination: {operation['destination']}")
        print()

def print_heading(heading):
    print(f"\n=== {heading} ===\n")

def confirm_action(prompt, auto_confirm=False):
    if auto_confirm:
        return True
    return input(f"{prompt} (y/n): ").lower() == "y"

def print_categories(categories):
    for category, filenames in categories.items():
        print(f"{category} ({len(filenames)}) {' '.join(filenames)}")

def print_files(files):
    for file in files:
        print(file)

def print_progress(current, total, filename):
    print(f"[{current}/{total}] {filename}")

def print_summary(summary):
    print_heading("SUMMARY")
    for key, value in summary.items():
        print(f"{key.capitalize()}: {value}")

def print_error(message):
    print(f"ERROR:{message}")

def print_welcome():
    print("=============\n")
    print("Batch File Organizer v1.0\n")
    print("=============\n")

def print_log_saved(log_path):
    print(f"Log saved to: {log_path}")

def print_file_count(count):
    print(f"Found: {count} files")

def print_execution_report(result):
    print("=== EXECUTION REPORT ===\n")
    print(f"Files renamed: {result['renamed']}")
    print(f"Failed: {result['failed']}")