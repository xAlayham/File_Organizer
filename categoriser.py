import os

files = [
    "holiday.jpg",
    "report.pdf",
    "notes.txt",
    "script.py",
    "image.png"
]

def file_category(filename):
    fname, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext == ".jpg" or ext == ".png":
        return "Image"
    elif ext == ".pdf" or ext == ".txt":
        return "Document"
    elif ext == ".py":
        return "Code"
    else:
        return "Other"
    
def categorise_files(files):
    organised_files = {}
    for file in files:
        category = file_category(file)
        if category not in organised_files:
            organised_files[category] = []
        organised_files[category].append(file)    
    return organised_files

def count_categories(categories):
    counts = {}
    for category in categories:
        counts[category] = len(categories[category])
    return counts

