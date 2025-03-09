def display_progress(completed, current, next_items, current_index, total):
    """
    Displays overall progress and a status table in the console.
    
    Args:
        completed (list): List of file paths that have been processed.
        current (str): File path currently in progress.
        next_items (list): List of file paths remaining.
        current_index (int): Number of files processed so far.
        total (int): Total number of files.
    """
    # Calculate overall progress percentage
    percent = (current_index / total) * 100 if total > 0 else 0
    progress_bar_length = 20
    filled_length = int(progress_bar_length * current_index // total) if total > 0 else 0
    progress_bar = '[' + '#' * filled_length + ' ' * (progress_bar_length - filled_length) + ']'
    
    print("\n" + "="*60)
    print(f"Overall Progress: {progress_bar} ({current_index} of {total} files, {percent:.1f}%)")
    print("-" * 60)
    print("Status Table:")
    print("{:<15} | {}".format("Status", "File Path"))
    print("-" * 60)
    for file in completed:
        print("{:<15} | {}".format("Completed", file))
    if current:
        print("{:<15} | {}".format("In Progress", current))
    for file in next_items:
        print("{:<15} | {}".format("Next", file))
    print("="*60 + "\n")
