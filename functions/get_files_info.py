import os
def get_files_info(working_directory, directory="."):
    abs_working_dir=os.path.abspath(working_directory)
    abs_directory=os.path.abspath(os.path.join(working_directory, directory))
    if not abs_directory.startswith(abs_working_dir):
        return f'Error: "{directory}" is not in the working directory'
    
    final_respone=""
    contents=os.listdir(abs_directory)
    for content in contents:
        content_path=os.path.join(abs_directory, content)
        is_dir=os.path.isdir(content_path)
        size=os.path.getsize(content_path)
        final_respone+=f"{content_path} is a {'directory' if is_dir else 'file'} with size {size} bytes\n"
    return final_respone