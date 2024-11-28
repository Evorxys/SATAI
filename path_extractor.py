import os

def display_files_in_directory(directory_path, level=0):
    """
    Recursively displays all files and subdirectories in a user-friendly, indented format.

    Args:
        directory_path (str): The path to the directory.
        level (int): Current indentation level (used for recursion).
    """
    try:
        # List all items in the directory
        items = os.listdir(directory_path)
    except PermissionError:
        print(" " * (level * 4) + "[Access Denied]")
        return

    for item in items:
        item_path = os.path.join(directory_path, item)
        
        # Check if it is a directory
        if os.path.isdir(item_path):
            print(" " * (level * 4) + f"[Folder] {item}")
            display_files_in_directory(item_path, level + 1)  # Recurse into the folder
        else:
            print(" " * (level * 4) + f"- {item}")  # Print file with indentation

if __name__ == "__main__":
    folder_path = input("Enter the path of the folder: ")
    
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        print(f"\nContents of the folder '{folder_path}':")
        display_files_in_directory(folder_path)
    else:
        print("The provided path is not a valid directory.")
