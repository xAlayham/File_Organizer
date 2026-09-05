import os
from datetime import datetime

def get_timestamp() -> str:
    """Return the current date and time formatted for use in a filename."""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def create_log_file() -> str:
    """Create the logs directory and return a path for a new log file."""
    os.makedirs("logs", exist_ok=True)

    timestamp = get_timestamp()
    path = os.path.join("logs", f"{timestamp}.log")

    return path   

def write_execution_log(log_path: str, folder: str, operations: list[dict], result: dict) -> None:
    """Write details of an organisation run to a log file."""
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
