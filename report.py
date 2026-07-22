def print_execution_report(result):
    print("=== EXECUTION REPORT ===\n")
    print(f"Files renamed: {result['renamed']}")
    print(f"Failed: {result['failed']}")
