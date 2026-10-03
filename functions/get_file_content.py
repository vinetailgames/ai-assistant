from config import CHAR_LIMIT
import os

def get_file_content(working_directory: str, file_path: str) -> str:
    # Check if the file_path is outside the working_directory
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # Check if the file exists and is a regular file
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_file_path, 'r') as f:
            content = f.read(CHAR_LIMIT)
            # Check if the file was larger than the limit
            if f.read(1):  # Try to read one more character to see if there's more content
                content += f'[...File "{file_path}" truncated at {CHAR_LIMIT} characters]'
            return content
    except Exception as e:
        return f'Error reading file "{file_path}": {str(e)}'