import os
import re


def extract_and_standardize_case_number(text):
    # Regular expression to match {number}/{year} or {number}-{year}
    pattern = r'(\d+)[-/](\d{4})'
    
    # Search for the pattern in the text
    match = re.search(pattern, text)
    
    if match:
        number, year = match.groups()
        # Replace / with - to standardize
        return f"{number}-{year}"
    return None

# Example usage
text = "SENTENZA sul  ricorso proposto da..."  # Change this to test different cases

result = extract_and_standardize_case_number(text)
if not result:
    print("Extracted Case Number:", result)
else:
    print("No valid case number found.")


# download_dir = os.path.join(os.getcwd(), "download", "2020")
# files = os.listdir(download_dir)
# # pattern = r"-2020(?: \(\d+\))?$"
# pattern = r"-2020(?: \()?$"
# # input_file = os.path.join(download_dir, "downloaded.txt")
# output_file = os.path.join(download_dir, "cleaned_downloaded.txt")

# with open(output_file, "r") as file:
#     downloaded = [line.strip() for line in file.readlines()]

# unique_lines = set()

# # Open input file, process, and write unique lines to output file
# with open(input_file, "r") as infile, open(output_file, "w") as outfile:
#     for line in infile:
#         cleaned_line = line.strip()
#         if not bool(re.search(pattern, cleaned_line)) and cleaned_line not in unique_lines:
#             unique_lines.add(cleaned_line)
#             outfile.write(cleaned_line + "\n")
# for file in files:
    
#     # if file.split(".")[-2].endswith("-2020") or file.split(".")[-2].endswith(")"):
#     #     os.remove(os.path.join(download_dir, file))
#     #     print(file)
#     if file not in downloaded:
#         with open(os.path.join(download_dir, "aaaa.txt"), "a") as f:
#             f.write(f"{file}\n")

# for item in downloaded:
#     if f"{item}.pdf" not in files:
#         print(item)

# download_dir = os.path.join(os.getcwd(), "download", "2020")
# filename = "Tribunale di Grosseto, Sentenza n. 668-2020 del 09-10-2020.pdf"
# old_path = os.path.join(download_dir, filename)
# new_path = os.path.join(download_dir, f"1.pdf")
# os.rename(old_path, new_path)

# Use a set to track unique lines
# unique_lines = set()

# # Open input file, process, and write unique lines to output file
# with open(input_file, "r") as infile, open(output_file, "w") as outfile:
#     for line in infile:
#         cleaned_line = line.strip()
#         if cleaned_line not in unique_lines:
#             unique_lines.add(cleaned_line)
#             outfile.write(cleaned_line + "\n")

# print(f"Processed file saved as {output_file} with duplicates removed.")

# filename = "Tribunale di Grosseto, Sentenza n. 668-2020 del 09-10-2020.pdf"

# print(os.path.exists(os.path.join(os.getcwd(), "download", "2020", filename)))