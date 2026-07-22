def print_operations(operations):
    for operation in operations:
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