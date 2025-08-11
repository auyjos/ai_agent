import os


def get_files_info(working_directory, directory="."):
    try:
        directory_path = os.path.abspath(os.path.join(working_directory, directory))
        
        if not directory_path.startswith(os.path.abspath(working_directory)):
            return  f'Error: Cannot list "{directory}" as it is outside the permitted working directory'


        if not os.path.exists(directory_path):
            return f'Error: "{directory}" does not exist'
        if not os.path.isdir(directory_path):
            return f'Error: "{directory}" is not a directory'
        contents = os.listdir(directory_path)
        result = []
        for item in contents:
            item_path = os.path.join(directory_path, item)
            is_dir = os.path.isdir(item_path)
            file_size = os.path.getsize(item_path) if not is_dir else 0
            result.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(result)
    except Exception as e:
        return f"Error: {str(e)}"

