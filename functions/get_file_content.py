import os

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        # Resolve the absolute path of the file
        absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Ensure the file is within the working directory
        if not absolute_file_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Ensure the path is a file
        if not os.path.isfile(absolute_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read the file content
        with open(absolute_file_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)

        # Check if the file was truncated
        if os.path.getsize(absolute_file_path) > MAX_CHARS:
            content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        # Catch any unexpected errors and return them as a string
        return f"Error: {str(e)}"