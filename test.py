import unittest
import tempfile
import os
import shutil
from organize import organize_files, file_types, get_folder_summary

class TestOrganizeFiles(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory and set up the environment
        self.test_dir = tempfile.TemporaryDirectory()

        # Create test files
        self.files_to_create = [
            'test.jpg', 'test.docx', 'test.pdf', 'test.py', '.DS_Store', 'script.sh'
        ]
        self.folders_to_create = [
            'Images', 'Documents', 'ETC'
        ]

        # Create files in the temporary directory
        for file in self.files_to_create:
            open(os.path.join(self.test_dir.name, file), 'a').close()

        # Create folders
        for folder in self.folders_to_create:
            os.makedirs(os.path.join(self.test_dir.name, folder), exist_ok=True)

    def tearDown(self):
        # Clean up the temporary directory after the test
        self.test_dir.cleanup()

    def helper_organize_files(self):
        # Run the organize_files function
        organize_files(self.test_dir.name)


    def test_get_folder_summary(self):
        initial_summary = get_folder_summary(self.test_dir.name)
        print(initial_summary)
        self.helper_organize_files()
        final_summary = get_folder_summary(self.test_dir.name)
        print(final_summary)

        # Verify that the number of total files has decreased after organizing, which in this case, is to be zero.
        initial_total_files = int(self._extract_value(initial_summary, "Total files"))
        final_total_files = int(self._extract_value(final_summary, "Total files"))
        self.assertLess(final_total_files, initial_total_files, "Total number of files should decrease after organizing.")

        # Verify that the total number of folders has increased (since files have been organized into folders)
        initial_total_folders = int(self._extract_value(initial_summary, "Total folders"))
        final_total_folders = int(self._extract_value(final_summary, "Total folders"))
        self.assertGreater(final_total_folders, initial_total_folders, "Total number of folders should increase after organizing.")


    def _extract_value(self, summary, keyword):
        # Helper function to extract a value corresponding to a keyword from the summary text
        for line in summary.splitlines():
            if keyword in line:
                return line.split(":")[1].strip()
        return None
    

    def test_organize_files(self):
        self.helper_organize_files()

         # Verify the organized folder structure
        for folder_name, extensions in file_types.items():
            folder_path = os.path.join(self.test_dir.name, folder_name)
            if os.path.exists(folder_path):
                for filename in os.listdir(folder_path):
                    ext = os.path.splitext(filename)[1].lower()
                    self.assertIn(ext, extensions, f"{filename} should be in {folder_name}")

        # Verify the ETC folder
        etc_folder = os.path.join(self.test_dir.name, 'ETC')
        if os.path.exists(etc_folder):
            for filename in os.listdir(etc_folder):
                self.assertNotIn(filename, ['.DS_Store'], f"{filename} should not be a .DS_Store file")
                self.assertNotIn(os.path.splitext(filename)[1].lower(), [ext for exts in file_types.values() for ext in exts],
                                 f"{filename} should not be classified in the existing file types")


if __name__ == '__main__':
    unittest.main()
