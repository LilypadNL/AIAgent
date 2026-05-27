import os.path
from config.py import MAX_FILE_CONTENT_LENGTH

def get_file_content(working_directory: str, file_path: str) -> str:
    
    try: 
        #determine if file is in the working directory and that the working directory exists
        if not os.path.exists(working_directory):
            return f'    Error: Working directory does not exist'
        working_dir_abs = os.path.abspath(working_directory)
        
        tar_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if not os.path.commonpath([working_dir_abs, tar_file]) == working_dir_abs:
            return f'    Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(tar_file):
            return f'    Error: File not found or is not a regular file: "{file_path}"' 

        #read the file and return the content as a string
        with open (tar_file, 'r') as f:   
            file_content_string = f.read(MAX_FILE_CONTENT_LENGTH)
            if f.read(1): #check if there is more content in the file after reading the max length
                file_content_string += f'[...File "{file_path}" truncated at {MAX_FILE_CONTENT_LENGTH} characters]'

        return file_content_string
    
    except Exception as e:
        return f'    Error: {e}'