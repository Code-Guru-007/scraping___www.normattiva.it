# import requests
# import datetime
# import os

# SERVER_URL = os.getenv("SERVER_URL", "http://188.245.216.211")
# output_file = "unique_pdf_url.txt"

# with open("new.txt", 'r') as file:
#     filenames = [line.strip() for line in file.readlines()]
# index = 1
# for filename in filenames:
#     print(f"[ {index} / {len(filenames)}]")
#     index += 1
#     date = filename.split("_")[0]
#     requests.post(f"{SERVER_URL}:8000/api/sentenze_cassazione", json={
#         "fileName": filename,
#         "status": True,
#         "fileLink": f"2025/{date[:4]}-{date[4:6]}-{date[6:]}/{filename}",
#         "dateTime": datetime.datetime.now().isoformat()
#     })

# import re

# Input and output file paths
# input_file = "pdf_url.txt"
# output_file = "cleaned_pdf_url.txt"

# # Open the input file and process each line
# with open(input_file, "r") as infile, open(output_file, "w") as outfile:
#     for line in infile:
#         # Remove everything before and including "./"
#         cleaned_line = re.sub(r".*?(\./)", "", line.strip())  
        
#         # Replace "/" with "_"
#         cleaned_line = cleaned_line.replace("/", "_")
        
#         # Write to output file
#         outfile.write(cleaned_line + "\n")

# print(f"Processed lines have been saved to {output_file}")

input_file = "pdf_url.txt"
output_file = "unique_pdf_url.txt"

# Use a set to track unique lines
unique_lines = set()

# Open input file, process, and write unique lines to output file
with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        cleaned_line = line.strip()
        if cleaned_line not in unique_lines:
            unique_lines.add(cleaned_line)
            outfile.write(cleaned_line + "\n")

print(f"Processed file saved as {output_file} with duplicates removed.")