import renamer, categoriser

def build_plan(files, prefix):
    plan = []
    i = 1
    for file in files:
        new_file = renamer.rename_files(file, i, prefix)
        tuple = (file, new_file)
        plan.append(tuple)
        i += 1
    return plan

def build_move_plan(files):
    plan = []
    for filename in files:
        category = categoriser.file_category(filename)
        tuple = (filename, category)
        plan.append(tuple)
    return plan

def build_operations(files, prefix):
    operations = []
    i = 1
    for filename in files:
        plan = {}
        new_file = renamer.rename_files(filename, i, prefix)
        category = categoriser.file_category(filename)
        plan["old"] = filename
        plan["new"] = new_file
        plan["destination"] = category
        i += 1
        operations.append(plan)
    return operations