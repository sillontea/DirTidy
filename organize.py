import os
import shutil
import argparse
import json

# Load file types from a JSON file
# If the JSON file is not found, create it with default values.
def load_file_types():
    try:
        with open('file_types.json', 'r') as file:
            default_file_types = json.load(file)
            return default_file_types
    except FileNotFoundError:
        default_file_types = {
            'Images': ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
            'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'],
            'Documents': ['.pdf', '.docx', '.xlsx', '.pptx', '.odt', '.rtf', '.md'],
            'Archives': ['.zip', '.rar', '.tar', '.gz', '.7z'],
            'Audio': ['.mp3', '.wav', '.aac', '.flac', '.ogg'],
            'Development': ['.py', '.js', '.h5', '.keras', '.txt', '.csv', '.json', '.pt', '.html'],
            'Executables': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.sh', '.bat'],
        }
        save_file_types(default_file_types)
        return default_file_types

# Save the current file types to a JSON file for persistence.
def save_file_types(file_types):
    with open('file_types.json', 'w') as file:
        json.dump(file_types, file, indent=4)

file_types = load_file_types()

# Organize files in the given folder by moving them into new categorized subfolders.
def organize_files(folder):
    etc_folder = os.path.join(folder, 'ETC')
    os.makedirs(etc_folder, exist_ok=True)
    
    for filename in os.listdir(folder):
        if filename == ".DS_Store":
            continue  # .DS_Store 파일은 무시
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path) or file_path.endswith('.app'):
            ext = os.path.splitext(filename)[1].lower()
            moved = False
            for folder_name, extensions in file_types.items():
                if ext in extensions:
                    target_folder = os.path.join(folder, folder_name)
                    os.makedirs(target_folder, exist_ok=True)
                    new_filename = unique_filename(target_folder, filename)
                    try:
                        shutil.move(file_path, os.path.join(target_folder, new_filename))
                        print(f'Moved {filename} to {folder_name}')
                        moved = True
                        break
                    except Exception as e:
                        print(f"Failed to move {filename}: {e}")
            
            if not moved:
                new_filename = unique_filename(etc_folder, filename)
                try:
                    shutil.move(file_path, os.path.join(etc_folder, new_filename))
                    print(f'Moved {filename} to ETC')
                except Exception as e:
                    print(f"Failed to move {filename}: {e}")
        
        # Folder handling
        # If the directory is not "ETC" and is not one of defined folder categories, moves into "ETC" folder.
        elif os.path.isdir(file_path) and filename != 'ETC' and not filename in file_types:
            # Move directories that do not match any other category to ETC
            new_dirname = unique_filename(etc_folder, filename)
            try:
                shutil.move(file_path, os.path.join(etc_folder, new_dirname))
                print(f'Moved directory {filename} to ETC')
            except Exception as e:
                print(f"Failed to move directory {filename}: {e}")

    remove_empty_folders(folder)


# Ensure unique filenames in the target folder by appending a counter if needed.
def unique_filename(target_folder, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(target_folder, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1

    return new_filename

# Remove any empty folders that may have been left after organizing files.
def remove_empty_folders(folder):
    for dirpath, dirnames, filenames in os.walk(folder, topdown=False):
        if not dirnames and not filenames:
            os.rmdir(dirpath)

# Generate a summary of files in the specified folder, excluding subfolders.
def get_folder_summary(folder):
    total_files = 0
    total_folders = 0
    folder_list = []
    file_list = []
    extensions = {}

    # Iterate through items in the folder
    items = os.listdir(folder)
    for item in items:
        item_path = os.path.join(folder, item)
        if os.path.isfile(item_path) or item_path.endswith('.app'):
            if item == ".DS_Store":
                continue  # .DS_Store 파일은 무시
            # Extract the file extension
            ext = os.path.splitext(item)[1].lower()
            extensions[ext] = extensions.get(ext, 0) + 1
            total_files += 1
            file_list.append(item_path)
        elif os.path.isdir(item_path):
            total_folders += 1
            folder_list.append(os.path.basename(item_path))

    # Generate the summary message
    summary_message = f"\n<<summary>>\nOrganizing directory: {folder}\nTotal folders: {total_folders}\n"
    for i, f in enumerate(folder_list):
        summary_message += f"   {i+1}) {f}\n"
    summary_message += f"Total files: {total_files}\n"
    for i, (ext, count) in enumerate(extensions.items()):
        summary_message += f"   {i+1}) {ext}: {count} files\n"

    return summary_message


def merge_directory(src_path, dest_path):
    """
    Merge the source directory into the destination directory.
    If the destination folder already exists and is a category folder, merge into it.
    """
    if os.path.exists(dest_path):
        _file_types = file_types.copy()
        _file_types['ETC'] = []

        # If the destination folder already exists, merge the folders that match category folders
        for valid_folder in _file_types:
            src_folder = os.path.join(src_path, valid_folder)
            dest_folder = os.path.join(dest_path, valid_folder)

            if os.path.exists(src_folder) and os.path.exists(dest_folder):
                # Merge two folders
                for item in os.listdir(src_folder):
                    if item == ".DS_Store":
                        continue  # Ignore .DS_Store
                    item_path = os.path.join(src_folder, item)
                    dest_item_path = os.path.join(dest_folder, item)
                    if os.path.exists(dest_item_path):
                        dest_item_path = unique_filename(dest_folder, item)
                    shutil.move(item_path, dest_item_path)
                print(f"moved '{src_folder}' into '{dest_folder}'.")
            elif os.path.exists(src_folder):
                shutil.move(src_folder, dest_folder)
                print(f"moved '{src_folder}' into '{dest_folder}'.")
        remove_empty_folders(src_path)
        print(f"\nMerged content from '{src_path}' into '{dest_path}'.\n")
    else:
        print("The destination path does not exist. Cannot merge.\n")


# Display the current file type categories and their associated extensions.
def display_file_types():
    print("Current file type settings:")
    print("(folder_name: types of files)")
    for folder_name, extensions in file_types.items():
        print(f"  - {folder_name}: {', '.join(extensions)}")

# Allow the user to modify the file type categories and their associated extensions.
def modify_file_types():
    while True:
        print("\nModify file types:")
        print("1. View current file types")
        print("2. Add extension to a category")
        print("3. Remove extension from a category")
        print("4. Exit modification")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            display_file_types()
        elif choice == '2':
            category = input("Enter the category to add an extension to: ")
            if category in file_types:
                extension = input("Enter the extension to add (e.g., .md): ").lower()
                if extension not in file_types[category]:
                    file_types[category].append(extension)
                    print(f"Added {extension} to {category}.")
                else:
                    print(f"{extension} is already in {category}.")
            else:
                print(f"Category '{category}' does not exist.")
        elif choice == '3':
            category = input("Enter the category to remove an extension from: ")
            if category in file_types:
                extension = input("Enter the extension to remove (e.g., .md): ").lower()
                if extension in file_types[category]:
                    file_types[category].remove(extension)
                    print(f"Removed {extension} from {category}.")
                else:
                    print(f"{extension} is not in {category}.")
            else:
                print(f"Category '{category}' does not exist.")
        elif choice == '4':
            save_file_types(file_types)
            break
        else:
            print("Invalid choice. Please try again.")

# Main function to execute the script functionality
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Organize files in a directory by their extensions.')
    parser.add_argument('--dir', type=str, required=True, help='Path to the directory to organize')
    parser.add_argument('--merge', type=str, required=False, help='Path to the directory to merge into the target directory')
    args = parser.parse_args()
    
    if os.path.isdir(args.dir):
        # Get the initial folder status
        initial_summary = get_folder_summary(args.dir)  
        print(initial_summary) # files by extensions

        display_file_types()
        print("Non-catergorized files and folders will move to ETC.")
        proceed = input("\nDo you want to proceed with these settings? (y/n): ").lower()
        if proceed == 'y':    
            print('\n')
            organize_files(args.dir) # organizing it
            print("Organized directory.\n")
            # When --merge argument is provided, 
            # merge organized directories into the appropriate category folder in --merge path.
            if args.merge and os.path.isdir(args.merge):
                merge_directory(args.dir, args.merge)

            final_summary = get_folder_summary(args.dir)  
            print(final_summary)

        elif proceed == 'n':
            print("You can modify the file type settings.")
            modify_file_types()
        else:
            print("Invalid input. Exiting.")
    else:
        print(f"Error: The path '{args.dir}' is not a valid directory.")