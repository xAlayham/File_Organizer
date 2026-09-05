import json

DEFAULTS = {
    "default_prefix": "backup",
    "show_summary": True,
    "run_tests": True,
}

def load_config(filepath: str = "config.json") -> dict:
    """Load configuration from a JSON file, falling back to defaults if loading fails."""
    try:
        with open(filepath) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Config file not found at {filepath}, using defaults.")
        return DEFAULTS.copy()
    except json.JSONDecodeError as e:
        print(f"Config file is malformed: {e}. Using defaults")
        return DEFAULTS.copy()

    merged = DEFAULTS.copy()
    merged.update(data)
    return merged