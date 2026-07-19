from datetime import datetime
import os

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def create_log_file():
    os.makedirs("logs", exist_ok=True)
    timestamp = get_timestamp()
    path = os.path.join("logs", f"{timestamp}.log")
    return path   

def write_execution_log(log_path, folder, operations, result):
    with open(log_path, "w") as f:
        f.write("Application started\n")
        f.write(f"Folder: {folder}\n\n")
        f.write("Operations:\n")
        for operation in operations:
            f.write(f"{operation['old']} -> {operation['new']} ({operation['destination']})\n")
        f.write("\nResult:\n")
        f.write(f"Renamed: {result['renamed']}\n")
        f.write(f"Failed: {result['failed']}\n\n")
        f.write("Application Finished\n")

