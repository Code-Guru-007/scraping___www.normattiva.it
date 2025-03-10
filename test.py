import os
import datetime
import requests

SERVER_URL = "http://188.245.216.211"  # Replace with your actual server URL

base_directory = os.path.join(os.getcwd(), "ilmerito.it", "download")  # Change this if the directories are not in the current working directory

for year in range(2010, 2025):
    year_directory = os.path.join(base_directory, str(year))
    
    if not os.path.exists(year_directory) or not os.path.isdir(year_directory):
        continue  # Skip if the directory doesn't exist
    current = 0
    posted_filelink = []
    if os.path.exists('posted.txt'):
        with open("posted.txt", "r") as file:
            posted_filelink = [line.strip() for line in file.readlines()]
    for file in os.listdir(year_directory):
        current += 1
        file_path = os.path.join(year_directory, file)

        if not os.path.isfile(file_path):
            continue  # Skip if it's not a file
        
        filename = file
        # if file.lower().endswith(".doc"):
        #     filename = file.rsplit(".", 1)[0] + ".pdf"  # Change .doc to .pdf in filename
        if not filename.endswith(".pdf"):
            continue
        file_link = f"{year}/{filename}"
        
        if file_link in posted_filelink:
            print("Already Posted !")
            continue

        payload = {
            "fileName": filename,
            "status": True,
            "fileLink": file_link,
            "dateTime": datetime.datetime.now().isoformat()
        }

        requests.post(f"{SERVER_URL}:8000/api/ilmerito.it", json=payload)
        
        with open('posted.txt', 'a') as file:
            file.write(f"{file_link}\n")
        
        print(f"[{year} ==>   {current}  /  {len(os.listdir(year_directory))}]")



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

# # Input and output file paths
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

# import os
# import ftplib

# # FTP Credentials
# FTP_HOST = "109.205.183.137"
# FTP_USER = "legal_doc@db-legale.professionista-ai.com"
# FTP_PASS = "G}SsFa@dB@&3"


# # Base remote directory
# FTP_BASE_DIR = "/sentenze_merito/downloaded"

# # Initialize file counter
# uploaded_file_count = 0

# # Connect to FTP server
# ftp = ftplib.FTP(FTP_HOST)
# ftp.login(FTP_USER, FTP_PASS)

# def ensure_ftp_directory_exists(directory):
#     """Ensure the directory exists on the FTP server, create if not."""
#     directories = directory.split("/")
#     for i in range(len(directories)):
#         path = "/".join(directories[: i + 1])  # Build path step by step
#         try:
#             ftp.cwd(path)  # Try changing to the directory
#         except ftplib.error_perm:
#             ftp.mkd(path)  # Create the directory if it doesn’t exist
#             ftp.cwd(path)

# def upload_pdfs(local_dir, remote_dir):
#     """Recursively find and upload PDF files from local directory to FTP server."""
#     global uploaded_file_count  # Use global variable to track count

#     ensure_ftp_directory_exists(remote_dir)  # Ensure remote directory exists

#     for root, _, files in os.walk(local_dir):
#         # relative_path = local_dir.split('\\')[-1]  # Preserve structure within the year folder
#         # target_ftp_dir = os.path.join(remote_dir, relative_path).replace("\\", "/")  # Convert to FTP path
#         target_ftp_dir = remote_dir
#         print(target_ftp_dir)
        
#         ensure_ftp_directory_exists(target_ftp_dir)  # Ensure subdirectories exist

#         pdf_files = ftp.nlst()
#         for file in files:
#             if file.endswith(".pdf"):  # Only upload PDF files
#                 local_file_path = os.path.join(local_dir, file)
#                 if file in pdf_files:
#                     uploaded_file_count += 1
#                     print(f"Already Uploaded: {uploaded_file_count}  /  {len(files)}")
#                     continue
#                 with open(local_file_path, "rb") as f:
#                     ftp.storbinary(f"STOR {file}", f)
#                 uploaded_file_count += 1
#                 print(f"Uploaded: {uploaded_file_count}  /  {len(files)}")

#                 # Update count and print progress

# # Iterate through directories from 2015 to 2024
# for year in range(2010, 2025):
#     year_dir = os.path.join(os.getcwd(), str(year))
#     if os.path.exists(year_dir) and os.path.isdir(year_dir):
#         remote_year_dir = f"{FTP_BASE_DIR}/{year}"
#         upload_pdfs(year_dir, remote_year_dir)

# # Close FTP connection
# ftp.quit()
# print(f"\n Upload complete! Total files uploaded: {uploaded_file_count}")

# Gennaio
# febbraio
# Marzo
# aprile
# Maggio
# Giugno
# Luglio
# agosto
# settembre
# ottobre
# novembre
# dicembre

from datetime import datetime, timedelta

date_string = "2025-02-28"
date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

current_date = datetime.today().date()
difference = (current_date - date_object).days

if difference > 16:
    print("passed")
else:
    print("not passed")
