import scanner, categoriser

folder = input("Enter a folder: ")
files = scanner.scan_folder(folder)


if files is None:
    print("Folder not found.")
else:
    files = categoriser.categorise_files(files)
    category_count = categoriser.count_categories(files)
    print(f"Found: {len(files)} files")
    for category, filenames in files.items():
        print(f"{category} ({len(filenames)}) {' '.join(filenames)}")