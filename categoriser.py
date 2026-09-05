import os

def file_category(filename: str) -> str:
    """Return the category a file belongs to, based on its extension."""
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext in (".jpg", ".png"):
        return "Image"
    elif ext in (".pdf", ".txt"):
        return "Document"
    elif ext == ".py":
        return "Code"
    else:
        return "Other"

def categorise_files(files: list[str]) -> dict[str, list[str]]:
    """Group a list of filenames by their category."""
    organised_files = {}
    for file in files:
        category = file_category(file)
        if category not in organised_files:
            organised_files[category] = []
        organised_files[category].append(file)
    return organised_files

def count_categories(categories: dict[str, list[str]]) -> dict[str, int]:
    """Count how many files fall into each category."""
    counts = {}
    for category in categories:
        counts[category] = len(categories[category])
    return counts