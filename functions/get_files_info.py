import os.path

def get_files_info(working_directory: str, directory: str = ".") -> str:
    
    #use a try/except block for any errors raised by std library functions.
    try: 
    
        #Return an error if the directory is not a directory
        if not os.path.isdir(directory) or not os.path.exists(working_directory):
            raise ValueError(f'Error: "{directory}" is not a directory')
    
        #Check to see that directory is inside the working directory
        working_dir_abs = os.path.abspath(working_directory)
        tar_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        if not os.path.commonpath([working_dir_abs, tar_dir]) == working_dir_abs:
            raise ValueError(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    
    except Exception as e:
        return print(f'Error: {e}')


    #Success, target directory is valid and in the working directory
    else: 
        return print(f'Success: "{directory}" is within the working directory')
    
