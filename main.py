import scanner, categoriser, planner, executor, report, logger

folder = input("Enter a folder: ")
files = scanner.scan_folder(folder)
prefix = "backup"

if files is None:
    print("Folder not found.")
else:
    categories = categoriser.categorise_files(files)
    print(f"Found: {len(files)} files")
    for category, filenames in categories.items():
        print(f"{category} ({len(filenames)}) {' '.join(filenames)}")
    operations = planner.build_operations(files, prefix)
    print("=== OPERATION REVIEW ===\n")
    for operation in operations:
        print(f"Old: {operation['old']}")
        print(f"New: {operation['new']}")
        print(f"Destination: {operation['destination']}")
        print()
    
    choice_rename = input("Proceed with rename? (y/n)").lower()
    if choice_rename == "y":
        rename_result = executor.execute_plan(folder, operations)
        report.print_execution_report(rename_result)
        
        log_path = logger.create_log_file()
    
        logger.write_execution_log(log_path, folder, operations, rename_result)

        print(f"Log saved to: {log_path}")


    files = scanner.scan_folder(folder)
    print("\n=== NEW FOLDER CONTENTS ===")
    for file in files:
        print(file)

