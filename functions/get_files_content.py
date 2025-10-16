import os

max_chars=10000

def get_files_content(working_directory, file_path):
    abs_working_dir=os.path.abspath(working_directory)
    abs_file_path=os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: "{file_path}" is not in the working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a file'
    file_content_strings=""
    try:
        with open(abs_file_path, 'r') as f:
            file_content_strings=f.read(max_chars)
            if len(file_content_strings)>max_chars:
                file_content_strings+=("file truncated")
            return file_content_strings
    except Exception as e:
        return f'Exception reading file: {e}'
        

    