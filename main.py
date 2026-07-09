import scanner

folder = input("Enter a folder: ")
files = scanner.scan_folder(folder)

if files is None:
    print("Folder not found.")
else:
    print(f"Found: {len(files)} files")
    print(files)