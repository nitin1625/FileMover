import os
import shutil
import re
import fnmatch
from pathlib import Path


# find out exclude files and folders 
def filter_exclusions(source_path, filess, folders):
    exclude_files = []
    exclude_folders = []

    if not filess and not folders:
        return exclude_files, exclude_folders

    # Walk through the directory tree
    for root, dirs, files in os.walk(source_path):

        # Check folder exclusions
        for dir_name in dirs[:]:  # Iterate over a copy to safely modify `dirs`
            if any(fnmatch.fnmatch(dir_name, pattern) for pattern in folders):
                rel_path = os.path.relpath(os.path.join(root, dir_name), source_path)
                exclude_folders.append(rel_path)
                dirs.remove(dir_name)  # Remove directory to skip its traversal

        # Check file exclusions
        for file_name in files:
            if any(fnmatch.fnmatch(file_name, pattern) for pattern in filess):
                rel_path = os.path.relpath(os.path.join(root, file_name), source_path)
                exclude_files.append(rel_path)

    return exclude_files, exclude_folders


# include elemnts after exclusion
def give_include_list(source_directory, exclude_files, exclude_foldernames):
    # Get excluded files and folders using the helper function
    exclude_filenames, exclude_foldernames = filter_exclusions(source_directory, exclude_files, exclude_foldernames)
    # Combine exclude lists and convert to a set for faster lookups
    exclude_set = set(exclude_filenames + exclude_foldernames)
    print(exclude_set)

    # List to store items to keep
    keep_list = []

    if not exclude_set:
       keep_list.append('.')
       return keep_list

    # Walk through the directory and its subdirectories
    for dirpath, dirnames, filenames in os.walk(source_directory):
        # Get the relative path to the current directory
        relative_dirpath = os.path.relpath(dirpath, source_directory)

        # Skip current directory if it's in the exclude list
        if relative_dirpath in exclude_set and relative_dirpath != ".":
            dirnames.clear()  # Prevent traversal into this directory
            continue


        # Filter `dirnames` in-place to exclude unwanted directories
        dirnames[:] = [d for d in dirnames if os.path.join(relative_dirpath, d) not in exclude_set]

        # Add files in the current directory
        for filename in filenames:
            file_path = os.path.normpath(os.path.join(relative_dirpath, filename))
            if file_path not in exclude_set:
                keep_list.append(os.path.join(dirpath,filename))

    if '.' in keep_list:
        keep_list.remove('.')

    keep_list=[i.replace("\\", "/") for i in keep_list]

    return keep_list

# new name for existing files or folders
def get_unique_name(path):
    base, ext = os.path.splitext(path)
    counter = 1
    new_path = f"{base}_{counter}{ext}"
    while os.path.exists(new_path):
        counter += 1
        new_path = f"{base}_{counter}{ext}"
    return new_path

# main function
def copy_or_move_elements(source, destination, include_list, handle_existing, operation="copy"):
    # Iterate through each item in the include_list and copy or move them
    for root, dirs, files in os.walk(source):
        # Create directories in the destination corresponding to the source directory structure
        relative_dir = os.path.relpath(root, source).replace("\\", "/")
        dest_dir = os.path.join(destination, relative_dir).replace("\\", "/")
        
        # Ensure the directory exists in the destination
        if not os.path.exists(dest_dir):
            print(f"Directory does not exist, creating: {dest_dir}")
            os.makedirs(dest_dir, exist_ok=True)
        
        # Process each file in the current directory
        for file_name in files:
            # Get the full path of the source file
            source_file_path = os.path.join(root, file_name).replace("\\", "/")
            
            # Check if the file is in the include list
            if source_file_path in include_list or '.' in include_list:
                dest_file_path = os.path.join(dest_dir, file_name).replace("\\", "/")
                
                # Check if file already exists at destination
                if os.path.exists(dest_file_path):
                    if handle_existing == "skip":
                        print(f"Skipped (already exists): {dest_file_path}")
                        continue
                    elif handle_existing == "rename":
                        dest_file_path = get_unique_name(dest_file_path)
                        print(f"Renamed to: {dest_file_path}")
                    elif handle_existing == "overwrite":
                        if os.path.isdir(dest_file_path):
                            print(f"{dest_file_path} exists as a folder, removing it.")
                            shutil.rmtree(dest_file_path)  # Remove folder
                        else:
                            print(f"{dest_file_path} exists as a file, removing it.")
                            os.remove(dest_file_path)  # Remove file
                
                # Perform the operation (copy or move)
                if operation == "copy":
                    shutil.copy(source_file_path, dest_file_path)  # Copy file
                    print(f"Copied '{source_file_path}' to '{dest_file_path}'")
                elif operation == "move":
                    shutil.move(source_file_path, dest_file_path)  # Move file
                    print(f"Moved '{source_file_path}' to '{dest_file_path}'")
            
            else:
                # This file is excluded from being copied but create the directory for it
                print(f"Excluded (file is not in include list): {source_file_path}")
        
    print(f"Operation '{operation}' completed successfully.")

# validate destination path
def handle_destination_path():
    while True:
        # Initial input of destination path
        destination_path = input("Enter the destination folder path: ").strip()
        
        # Check if path exists
        if os.path.exists(destination_path):
            # Verify it's a directory and writable
            if os.path.isdir(destination_path):
                if os.access(destination_path, os.W_OK):
                    return destination_path
                else:
                    print(f"Error: No write permission for '{destination_path}'.")
            else:
                print(f"Error: '{destination_path}' is not a directory.")
        else:
            # Path doesn't exist - provide options
            print(f"\nWarning: Destination path '{destination_path}' does not exist.")
            print("You have three options:")
            print("1. Create the directory")
            print("2. Enter a different path")
            print("3. Cancel operation")
            
            # Get user choice
            while True:
                choice = input("Enter your choice (1/2/3): ").strip()
                
                if choice == '1':
                    # Attempt to create directory
                    try:
                        # Try to create full path
                        if not os.path.exists(destination_path):
                            os.makedirs(destination_path, exist_ok=True)
                            print(f"Created directory: {destination_path}")
                            return destination_path
                    except PermissionError:
                        print("Error: No permission to create directory.")
                        # Continue to choice loop
                    except Exception as e:
                        print(f"Error creating directory: {e}")
                        # Continue to choice loop
                
                elif choice == '2':
                    # Break inner loop to re-enter path
                    break
                
                elif choice == '3':
                    # Exit entire function
                    print("Operation cancelled.")
                    return None
                
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")


# validate source path
def validate_source_path(path):
    try:
        # Check if path exists
        if not os.path.exists(path):
            print(f"Error: The source path '{path}' does not exist.")
            return False
        
        # Check if path is readable
        if not os.access(path, os.R_OK):
            print(f"Error: No read permission for the source path '{path}'.")
            return False
        
        # Check if path is a directory
        if not os.path.isdir(path):
            print(f"Error: The source path '{path}' is not a directory.")
            return False
        
        # Check if directory is empty
        if not os.listdir(path):
            print(f"Warning: The source directory '{path}' is empty.")
        
        return True
    except Exception as e:
        print(f"Error verifying source path: {e}")
        return False

# validate input items 
def get_valid_input(prompt, validation_func, error_message):
    while True:
        user_input = input(prompt).strip()
        if user_input and validation_func(user_input):
            return user_input
        if not user_input:
            print("Input cannot be empty.")

# validate input functions  
def validate_operation(operation):
    """Check if operation is valid."""
    return operation in {"1", "2"}

def validate_include(include):
    """Check if include option is valid."""
    return include in {"1", "2", "3"}

def validate_handle_existing(validate_handle):
    """Check if validate_handle option is valid."""
    return validate_handle in {"1", "2", "3"}


#  function to get input 
def main():
    # Get source path with verification
    source_path = get_valid_input(
        "Enter the source folder path: ", 
        validate_source_path, 
        "Invalid source path. Please try again."
    )

    # Get destination path with comprehensive handling
    destination_path = handle_destination_path()
    
    # Check if operation was cancelled
    if destination_path is None:
        print("Operation cancelled.")
        return


    exclude_filenames=[]
    exclude_foldernames=[]
    
    # Get exclude filename patterns
    print("\nExclude Filename Patterns (Space Seperated) :")
    exclude_filenames = list(map(str , input().split()))
    
    # Get exclude folder name patterns
    print("\nExclude Folder Name Patterns (Space Seperated) :")
    exclude_foldernames = list(map(str , input().split()))

    # what to do with existing files/folders
    print("\nSelect how to Handle existing items:")
    print("1. overwrite")
    print("2. skip")
    print("3. rename")

    handle_existing = get_valid_input(
        "Enter option (1, 2, or 3 ): ", 
        validate_handle_existing, 
        "Invalid input. Please enter '1', '2' or '3'."
    )
    handle_existing_name = {
        "1": "overwrite", 
        "2": "skip", 
        "3": "rename"
    }[handle_existing]


     # what to do with existing files/folders
    print("\nSelect operation to do :")
    print("1. move")
    print("2. copy")

    operation = get_valid_input(
        "Enter option (1 or 2 ): ", 
        validate_operation, 
        "Invalid input. Please enter '1' or '2'."
    )
    handle_operation = {
        "1": "copy", 
        "2": "move"
    }[operation]


    source_path = source_path.replace("\\", "/")
    destination_path = destination_path.replace("\\", "/")

    

    include_list = give_include_list(source_path,exclude_filenames,exclude_foldernames )
    copy_or_move_elements(source_path, destination_path, include_list, handle_existing, handle_operation)


if __name__ == "__main__":
    main()