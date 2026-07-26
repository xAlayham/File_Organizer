files = ["a", "b", "c"]

total = len(files)

for i, file in enumerate(files, start=1):
    print(f"[{i}/{total}] Processing {file}")