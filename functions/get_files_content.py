import os
from google.genai import types
from pathlib import Path
max_chars=10000

def get_files_content(working_directory, file_path,max_chars=10000):
    working_path = Path(working_directory).resolve(strict=True)
    file_path_obj = Path(file_path)
    if file_path_obj.is_absolute():
         raise ValueError("Absolute paths not allowed")
    abs_file_path = (working_path / file_path).resolve(strict=True)
    abs_file_path.relative_to(working_path)  # Raises ValueError if outside
    if not abs_file_path.is_file():
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
schema_get_files_content = types.FunctionDeclaration(
name="get_files_content",
description="Get the contents of the given file as a string, constrained to the working directory.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="The path to the file to read, relative to the working directory.",
        ),
    },
),
)

