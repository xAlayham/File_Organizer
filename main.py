import scanner
import categoriser
import planner
import executor
import report
import logger
import config
import test_args
import system_logger
import display

system_logger.setup_logger()
system_logger.info("Application Started")

folder = test_args.args.folder
config_data = config.load_config()

prefix = test_args.args.prefix
show_summary = config_data["show_summary"]
run_tests = config_data["run_tests"]

system_logger.info("Scanning folder...")
files = scanner.scan_folder(folder)

if files is None:
    print("Folder not found.")
    system_logger.error("Folder not found")
else:
    system_logger.info(f"Found {len(files)} files")

    categories = categoriser.categorise_files(files)
    print(f"Found: {len(files)} files")
    display.print_categories(categories)        

    operations = planner.build_operations(files, prefix)
    display.print_heading("OPERATION REVIEW")
    display.print_operations(operations)
    
    if display.confirm_action("Proceed with rename?", auto_confirm=test_args.args.no_confirm):
        system_logger.info("Executing rename plan")

        rename_result = executor.execute_plan(folder, operations)
        report.print_execution_report(rename_result)
        
        log_path = logger.create_log_file()
        logger.write_execution_log(log_path, folder, operations, rename_result)
        print(f"Log saved to: {log_path}")

        system_logger.info("Execution complete")


    files = scanner.scan_folder(folder)
    display.print_heading("NEW FOLDER CONTENTS")
    display.print_files(files)