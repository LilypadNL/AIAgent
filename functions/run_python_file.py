import os.path
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        tar_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        #determine if file is in the working directory and that the working directory exists. Determine if the file is labeled as a Python file (.py).
        if not os.path.exists(working_directory):
            return f'Error: Working directory does not exist'
        if not os.path.commonpath([working_dir_abs, tar_file]) == working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(tar_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'        


    except Exception as e:
        return f'Error: {e}'
    
    try: 
        #Creating the command to run the in the subprocess
        command = ["python", tar_file]
        if args:
            command.extend(args)

        #Running the subprocess and capturing output and errors.
        capture = subprocess.run(command, capture_output = True, text = True, timeout = 30)
        if capture.returncode != 0:            
            return f'Error: Process exited with code {capture.returncode}: {capture.stderr}'
        if capture.stdout == None and capture.stderr == None:
            return f'Error: Process exited with code {capture.returncode}. No output produced.'
        else:
            return f'STDOUT: {capture.stdout}\nSTDERR: {capture.stderr}'


    except Exception as e:
        return f'Error: executing Python file: {e}'