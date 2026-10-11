import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a specified file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
                "file_path": {
                    "type": "string",
                    "description": "Path to the file within the specified directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                }
            },
            "required": ["file_path", "content"]
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        # Get absolute paths
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Check if the target file path is within the working directory
        valid_target_file = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Check if the target file path points to an existing directory
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Ensure all parent directories exist
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        # Write content to the file
        with open(target_file_path, "w") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {str(e)}'