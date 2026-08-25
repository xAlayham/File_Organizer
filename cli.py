import argparse

def parse_args() -> argparse.Namespace:
    """Parse and return the command-line arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument("folder")

    parser.add_argument(
        "--prefix",
        default="backup",
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

if __name__ == "__main__":
    args = parse_args()
    print(f"Folder: {args.folder}")
    print(f"Prefix: {args.prefix}")
    if args.dry_run:
        print("Dry Run Enabled")
    else:
        print("Real Execution")

    print(args.no_confirm)