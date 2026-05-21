from functions.get_files_info import get_files_info

#test cases
get_files_info("calculator", ".")
get_files_info("calculator", "/bin")
get_files_info("calculator", "../")
get_files_info("calculator", "main.py")

print(get_files_info("calculator", "."))
print(get_files_info("calculator", "pkg"))
print(get_files_info("calculator", "/bin"))
print(get_files_info("calculator", "../"))  