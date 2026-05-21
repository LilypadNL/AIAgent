import os.path
from os import listdir

def get_files_info(working_directory: str, directory: str = ".") -> str:
    
    #use a try/except block for any errors raised by std library functions.
    try: 
    
        #Return an error if the directory is not a directory
        
    
        #Check to see that directory is inside the working directory
        working_dir_abs = os.path.abspath(working_directory)
        tar_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if not os.path.commonpath([working_dir_abs, tar_dir]) == working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(tar_dir) or not os.path.exists(working_directory):
            return f'Error: "{directory}" is not a directory'
        
        #creating output string
        output_str = ""
        if directory == ".":
            output_str += "Result for current directory:\n"
        else: 
            output_str += f"Result for '{directory}' directory:\n"

        for file in os.listdir(tar_dir):
            isdir = os.path.isdir(os.path.join(tar_dir, file))
            size = os.path.getsize(os.path.join(tar_dir, file))
            output_str += f'  - {file}: file_size={size}, is_dir={isdir}\n'
        

        return output_str
        
    
    except Exception as e:
        return print(f'    Error: {e}')

    
    #Success, target directory is valid and in the working directory
    #else: 
    #    return print(f'Success: "{directory}" is within the working directory')
    

    