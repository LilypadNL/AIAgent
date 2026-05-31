import os.path
from os import makedirs
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites content to a specified file, creating intermediate directories if they do not exist",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write content to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file as a string",
            ),
        },
        required=["file_path", "content"]
    ),
)


def write_file(working_directory: str, file_path: str, content: str) -> str:

    try:    
        working_dir_abs = os.path.abspath(working_directory)
        tar_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        #determine if file is in the working directory and that the working directory exists
        if not os.path.exists(working_directory):
            return f'Error: Working directory does not exist'
        if not os.path.commonpath([working_dir_abs, tar_file]) == working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(tar_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory' 
        
        #starting writing to the file, creating intermediate directories if they do not exist
        os.makedirs(os.path.dirname(tar_file), exist_ok=True) 
        with open(tar_file, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'