import os
import subprocess
import sys
from google.genai import types

def run_python_file(working_directory: str, file_path: str, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: "{file_path}" is not in the working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a file'
    if not file_path.endswith(".py"):
        return f'Error:"{file_path}" is not a python file'
    try:
        python_executable = sys.executable or "python"
        final_args=[python_executable, file_path]
        final_args.extend(args)

        completed = subprocess.run(
            final_args,
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True,
            text=True,
        )

        if completed.stdout is None or completed.stderr is None:
            stdout_text = ""
            stderr_text = ""
        else:
            stdout_text = completed.stdout or ""
            stderr_text = completed.stderr or ""

        final_string = f"""
STDOUT:{stdout_text}
STDERR:{stderr_text}
"""
        if completed.returncode != 0:
            final_string += f"Process exited with code {completed.returncode}"
        if stdout_text == "" and stderr_text == "":
            final_string = "No output produced"

        return final_string
    except Exception as e:
        return f'Error: executing python file:{e}'
schema_run_python_file = types.FunctionDeclaration(
name="run_python_file",
description="Runs a Python file with the current interpreter. Accepts optional CLI args.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="The Python file to run, relative to the working directory",
        ),
        "args": types.Schema(
            type=types.Type.ARRAY,
            description="An optional array of strings to be used as the CLI args for the Python file",
            items=types.Schema(
                type=types.Type.STRING,
            )
        ),
    },
),
)
# import os
# import sys

# # Add parent directory to path to find secure_python_runner
# parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# if parent_dir not in sys.path:
#     sys.path.insert(0, parent_dir)

# from secure_python_runner import SecurePythonRunner
# from google.genai import types

# def run_python_file(working_directory: str, file_path: str, args: list = None) -> str:
#     """Agent-facing function"""
#     runner = SecurePythonRunner(working_directory=working_directory)
#     result = runner.run(file_path, args or [])
    
#     if result.error:
#         return f"❌ Error: {result.error}"
    
#     output = []
    
#     if result.stdout:
#         output.append(f"📤 Output:\n{result.stdout}")
    
#     if result.stderr:
#         output.append(f"⚠️  Errors:\n{result.stderr}")
    
#     # Status info
#     status = "✅ Success" if result.success else "❌ Failed"
#     output.append(f"{status} (exit code: {result.returncode}, time: {result.execution_time:.2f}s)")
    
#     return "\n\n".join(output)

# # Schema
# schema_run_python_file = types.FunctionDeclaration(
#     name="run_python_file",
#     description=(
#         "Executes a Python file in a secure sandbox with resource limits. "
#         "Maximum execution time: 30 seconds. "
#         "Maximum memory: 256MB. "
#         "Captures stdout and stderr. "
#         "Only works with .py files in the working directory."
#     ),
#     parameters=types.Schema(
#         type=types.Type.OBJECT,
#         properties={
#             "file_path": types.Schema(
#                 type=types.Type.STRING,
#                 description=(
#                     "Path to Python file relative to working directory. "
#                     "Examples: 'main.py', 'tests/test_calculator.py'. "
#                     "Must be a .py file. No absolute paths or '..' allowed."
#                 ),
#             ),
#             "args": types.Schema(
#                 type=types.Type.ARRAY,
#                 description=(
#                     "Optional command-line arguments passed to the script. "
#                     "Each argument is a separate string. "
#                     "Example: ['--verbose', 'input.txt']"
#                 ),
#                 items=types.Schema(type=types.Type.STRING),
#             ),
#         },
#         required=["file_path"],
#     ),
# )