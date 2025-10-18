import os
import subprocess
import sys


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

        if (completed.stdout or completed.stderr) is None:
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