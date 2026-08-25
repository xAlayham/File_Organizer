import json
import os 

HISTORY_FILE = ".file_organiser_history.json"

def save_history(folder: str, operations: list[dict]) -> None:
    """Save the latest organisation operation to a JSON file"""

    history_path = os.path.join(folder, HISTORY_FILE)

    with open(history_path, "w") as file:
        json.dump(operations, file, indent=4)

def load_history(folder: str) -> list[dict] | None:
    """Load the latest organisation operations from history file"""

    history_path = os.path.join(folder, HISTORY_FILE)

    if not os.path.exists(history_path):
        return None

    with open(history_path, "r") as file:
        return json.load(file)

def clear_history(folder: str) -> None:
    """Remove the saved organisation history."""

    history_path = os.path.join(folder, HISTORY_FILE)

    if os.path.exists(history_path):
        os.remove(history_path)