with open("2025.txt", "r") as file:
    unique_lines = list(dict.fromkeys(file.readlines()))
    
with open("2025.txt", "w") as file:
    file.writelines(unique_lines)