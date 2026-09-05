import argparse

def parse_args() -> argparse.Namespace:
    """Parse and return the command-line arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument("folder")

    parser.add_argument(
        "--prefix",
        default=None,
    )

    parser.add_argument(
        "--dry-run",
        action="store_true"
    )

    parser.add_argument(
        "--no-confirm",
        action="store_true"
    )

    parser.add_argument(
        "--check-duplicates",
        action="store_true"
    )

    parser.add_argument(
        "--undo",
        action="store_true"
    )

    return parser.parse_args()
