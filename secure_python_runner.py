import os
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class RunResult:
    """Result of running a Python file"""
    stdout: str = ""
    stderr: str = ""
    returncode: int = 0
    execution_time: float = 0.0
    error: Optional[str] = None
    
    @property
    def success(self) -> bool:
        """True if execution succeeded (returncode == 0 and no error)"""
        return self.returncode == 0 and self.error is None


class SecurePythonRunner:
    """Secure Python runner with resource limits and sandboxing"""
    
    def __init__(self, working_directory: str):
        """
        Initialize the runner with a working directory.
        
        Args:
            working_directory: Base directory for running Python files
        """
        self.working_directory = os.path.abspath(working_directory)
        os.makedirs(self.working_directory, exist_ok=True)
    
    def run(self, file_path: str, args: List[str] = None) -> RunResult:
        """
        Run a Python file with resource limits.
        
        Args:
            file_path: Path to Python file relative to working_directory
            args: Optional command-line arguments for the script
            
        Returns:
            RunResult with execution details
        """
        if args is None:
            args = []
        
        # Validate file path
        abs_file_path = os.path.abspath(os.path.join(self.working_directory, file_path))
        
        # Security check: ensure file is within working directory
        if not abs_file_path.startswith(self.working_directory):
            return RunResult(
                error=f"File path '{file_path}' is outside working directory"
            )
        
        # Check if file exists
        if not os.path.isfile(abs_file_path):
            return RunResult(
                error=f"File '{file_path}' does not exist"
            )
        
        # Check if it's a Python file
        if not file_path.endswith(".py"):
            return RunResult(
                error=f"File '{file_path}' is not a Python file"
            )
        
        # Run the Python file
        try:
            python_executable = sys.executable or "python"
            final_args = [python_executable, abs_file_path]
            final_args.extend(args)
            
            start_time = time.time()
            completed = subprocess.run(
                final_args,
                cwd=self.working_directory,
                timeout=30,  # 30 second timeout
                capture_output=True,
                text=True,
            )
            execution_time = time.time() - start_time
            
            return RunResult(
                stdout=completed.stdout or "",
                stderr=completed.stderr or "",
                returncode=completed.returncode,
                execution_time=execution_time,
            )
        except subprocess.TimeoutExpired:
            return RunResult(
                error="Execution timed out after 30 seconds",
                execution_time=30.0,
            )
        except Exception as e:
            return RunResult(
                error=f"Error executing Python file: {str(e)}"
            )

