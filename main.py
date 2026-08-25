import scanner
import categoriser
import planner
import executor
import logger
import config
import cli
import system_logger
import display
import duplicates
import undo
import history

system_logger.setup_logger()
system_logger.info("Application Started")
display.print_welcome()

args = cli.parse_args()
folder = args.folder

if args.undo:
    operations = history.load_history(folder)

    if operations is None:
        display.print_error("No undo history found")
    else:
        undone = undo.undo_operations(folder, operations)
        print(f"Undone {undone} operations")

        if undone > 0:
            history.clear_history(folder)

    exit()

config_data = config.load_config()

prefix = args.prefix
show_summary = config_data["show_summary"]
run_tests = config_data["run_tests"]

system_logger.info("Scanning folder...")
files = scanner.scan_folder(folder)

if files is None:
    display.print_error("Folder not found")
    system_logger.error("Folder not found")
else:
    system_logger.info(f"Found {len(files)} files")

    if args.check_duplicates:
        duplicate_files = duplicates.find_duplicates(folder)

        if duplicate_files:
            display.print_duplicates(duplicate_files)

    categories = categoriser.categorise_files(files)
    display.print_file_count(len(files))
    display.print_categories(categories)

    operations = planner.build_operations(files, prefix)
    display.print_heading("OPERATION REVIEW")
    display.print_operations(operations)
    
    if display.confirm_action("Proceed with rename?", auto_confirm=args.no_confirm):
        system_logger.info("Executing rename plan")

        rename_result = executor.execute_plan(folder, operations)
        display.print_execution_report(rename_result)
        
        log_path = logger.create_log_file()
        logger.write_execution_log(log_path, folder, operations, rename_result)
        display.print_log_saved(log_path)

        system_logger.info("Execution complete")


    files = scanner.scan_folder(folder)
    display.print_heading("NEW FOLDER CONTENTS")
    display.print_files(files)