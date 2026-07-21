import argparse

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

args = parser.parse_args()

print(f"Folder: {args.folder}")
print(f"Prefix: {args.prefix}")
if args.dry_run is True:
    print("Dry Run Enabled")
else:
    print("Real Execution")
print(args.no_confirm)