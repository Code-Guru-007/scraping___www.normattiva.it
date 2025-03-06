input_file = "downloaded.txt"
output_file = "unique_pdf_url.txt"

with open("downloaded.txt", "r") as file:
    downloaded_title

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