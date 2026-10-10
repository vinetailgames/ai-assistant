import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    if args is None:
        args = []
    try:
        # Get absolute paths
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Check if the target file path is within the working directory
        valid_target_file = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if the target file path points to an existing file
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Check if the target file path points to a Python file
        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Execute the Python file and capture output
        result = subprocess.run(
            ["python3", target_file_path] + args,
            capture_output=True,
            text=True,
            cwd=working_dir_abs,
            timeout=30
        )

        output = result.stdout.strip()
        error_output = result.stderr.strip()

        output_lines = []

        if result.returncode != 0:
            output_lines.append(f"Process exited with code {result.returncode}")
        if output:
            output_lines.append(f"STDOUT: {output}")
        if error_output:
            output_lines.append(f"STDERR: {error_output}")
        if not output_lines:
            return "No output produced"
        return "\n".join(output_lines)

    except subprocess.TimeoutExpired:
        return "Error: Execution timed out"
    except Exception as e:
        return f'Error: {str(e)}'