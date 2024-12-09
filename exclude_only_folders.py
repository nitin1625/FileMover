import os
import shutil
import re
import fnmatch
from pathlib import Path



# find out exclude files and folders 
def filter_exclusions(source_path, folders):
    exclude_folders = []

    if  not folders:
        return  exclude_folders

    # Walk through the directory tree
    for root, dirs, files in os.walk(source_path):

        # Check folder exclusions
        for dir_name in dirs[:]:  # Iterate over a copy to safely modify `dirs`
            if any(fnmatch.fnmatch(dir_name, pattern) for pattern in folders):
                rel_path = os.path.relpath(os.path.join(root, dir_name), source_path)
                exclude_folders.append(rel_path)
                dirs.remove(dir_name)  # Remove directory to skip its traversal

    return exclude_folders
    
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
def copy_or_move_elements(source, destination, exclude_folders, handle_existing, operation="copy"):
    for root, dirs, files in os.walk(source):
        # Exclude folders in exclude_folders list from being processed
        dirs[:] = [d for d in dirs if os.path.join(root, d).replace("\\", "/") not in exclude_folders]
        
        # Create directories in the destination corresponding to the source directory structure
        relative_dir = os.path.relpath(root, source).replace("\\", "/")
        dest_dir = os.path.join(destination, relative_dir).replace("\\", "/")
        
        # Ensure the directory exists in the destination
        if not os.path.exists(dest_dir):
            print(f"Directory does not exist, creating: {dest_dir}")
            os.makedirs(dest_dir, exist_ok=True)

        # Process directories that are not excluded
        for dir_name in dirs:
            source_dir_path = os.path.join(root, dir_name).replace("\\", "/")
            dest_dir_path = os.path.join(dest_dir, dir_name).replace("\\", "/")
            
            # Check if directory already exists at destination
            if os.path.exists(dest_dir_path):
                if handle_existing == "skip":
                    print(f"Skipped (directory exists): {dest_dir_path}")
                    continue
                elif handle_existing == "rename":
                    dest_dir_path = get_unique_name(dest_dir_path)
                    print(f"Renamed directory to: {dest_dir_path}")
                elif handle_existing == "overwrite":
                    print(f"Overwriting existing directory: {dest_dir_path}")
                    shutil.rmtree(dest_dir_path)  # Remove existing directory
                
            # Perform the operation (copy or move)
            if operation == "copy":
                shutil.copytree(source_dir_path, dest_dir_path)  # Copy directory
                print(f"Copied directory '{source_dir_path}' to '{dest_dir_path}'")
            elif operation == "move":
                shutil.move(source_dir_path, dest_dir_path)  # Move directory
                print(f"Moved directory '{source_dir_path}' to '{dest_dir_path}'")



         # Process files in the current directory (those not excluded)
        for file_name in files:
            source_file_path = os.path.join(root, file_name).replace("\\", "/")
            dest_file_path = os.path.join(dest_dir, file_name).replace("\\", "/")
            
            # Check if file already exists at destination
            if os.path.exists(dest_file_path):
                if handle_existing == "skip":
                    print(f"Skipped (file exists): {dest_file_path}")
                    continue
                elif handle_existing == "rename":
                    dest_file_path = get_unique_name(dest_file_path)
                    print(f"Renamed file to: {dest_file_path}")
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
                print(f"Copied file '{source_file_path}' to '{dest_file_path}'")
            elif operation == "move":
                shutil.move(source_file_path, dest_file_path)  # Move file
                print(f"Moved file '{source_file_path}' to '{dest_file_path}'")


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
def exclude_only_folders():
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
    
        
        source_path = source_path.replace("\\", "/")
        destination_path = destination_path.replace("\\", "/")
    
        
        exclude_foldernames = filter_exclusions(source_path, exclude_foldernames)
        exclude_foldernames=[os.path.join(source_path,i).replace("\\", "/") for i in exclude_foldernames]
        copy_or_move_elements(source_path, destination_path, exclude_foldernames, handle_existing, operation="copy")
    
    
exclude_only_folders()