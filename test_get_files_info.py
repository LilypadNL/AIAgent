from functions.get_files_info import get_files_info

#test cases
get_files_info("calculator", ".")
get_files_info("calculator", "/bin")
get_files_info("calculator", "../")
get_files_info("calculator", "main.py")