# Organize Files CLI

This project provides a command-line tool to organize files within a specified directory based on their file types. Files are moved into folders categorized by type (e.g., Images, Documents), and uncategorized files are moved to an `ETC` folder. This script is especially useful for keeping download or workspace folders tidy.

## Code Introduction

The `organize.py` script categorizes files based on their extensions. It creates specific folders for each type (e.g., `Images`, `Documents`, `Videos`) and moves the files accordingly. The script also places uncategorized files in an `ETC` folder. Additionally, it includes functionality to ignore certain files (e.g., `.DS_Store`) and to handle merging directories if the target directory already contains categorized folders.

### Features
- **Categorize Files by Type**: Moves files into folders based on file extensions.
- **Merge Existing Folders**: If folders for specific categories already exist, files are merged without duplication.
- **ETC Folder**: Uncategorized files are moved to an `ETC` folder for easy identification.

The `test.py` script provides unit tests for `organize.py`, using temporary directories to ensure the script works as expected without modifying actual user files.


## Future Work

- **GUI Interface Development**: Develop a GUI interface to improve user experience.
- **Installer Creation**: Create an installer to make the application more user-friendly.

## Questions and Feedback

We welcome any questions, ideas, bug reports, or suggestions for improvements. Your feedback is invaluable in making this tool better. Please feel free to reach out through the issues section of this repository.


## File Type Customization

You can modify the file types and their corresponding folders using the command-line interface or by editing the `file_types.json` file.

### 1) Command-Line Interface
When running the script, you can view the current file type settings and, if you choose 'n', a menu will appear allowing you to modify the settings. Here, you can add or remove file extensions from existing categories.

```
You can modify the file type settings.

Modify file types:
1. View current file types
2. Add extension to a category
3. Remove extension from a category
4. Exit modification
```

### 2) Edit JSON File Directly
If you want to create personalized categories that are not part of the default, you can edit the `file_types.json` file directly. This file contains the mappings of file extensions to folder names, allowing you to easily customize how files are organized. Simply open the `file_types.json` file and add, remove, or modify the file extensions to suit your needs.

For example, to add `.rtf` files to the `Documents` category, you can modify the `file_types.json` as follows:

```json
{
    "Documents": [".pdf", ".docx", ".txt", ".rtf"]
}
```

## Usage Example
To use the script, run the following command:

### Organize Files Manually

```bash
python organize.py --dir /path/to/directory
```

This command will organize all the files in the specified directory into categorized folders. If a folder for a specific type already exists, the script will merge the content appropriately.

  
### Example

```bash
python organize.py --dir ~/Downloads
```

This will organize your `Downloads` folder by grouping files into folders such as `Images`, `Documents`, `ETC`, etc.

### Automate with Cron Job (Linux/macOS)

You can set up a cron job to automatically run the script periodically to keep your folders organized.
This will ensure that your specified directory is organized daily without manual intervention.

## Directory Description

- **organize.py**: Main script to organize files within a directory.
- **test.py**: Contains unit tests for validating the functionality of `organize.py`.
- **LICENSE**: MIT License file that provides licensing information for the project.
- **README.md**: Documentation file containing an overview of the project, usage examples, and additional details.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.