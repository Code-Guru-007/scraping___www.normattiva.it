import os
from datetime import datetime, timedelta
import requests

# Configurable server URL and endpoint
SERVER_URL = "http://188.245.216.211"
PORT = 8000  # Change this if needed
base_directory = os.path.join(os.getcwd(), "download")

posted_filelink = []
if os.path.exists("posted.txt"):
    with open("posted.txt", "r") as file:
        posted_filelink = [line.strip() for line in file.readlines()]


def find_pdfs(directory, year):
    pdf_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                relative_path = os.path.relpath(root, directory)  # Get relative subdirectory path
                if relative_path == ".":
                    file_link = f"{year}/{file}"
                else:
                    file_link = f"{year}/{relative_path}/{file}"
                pdf_files.append((os.path.join(root, file), file_link))
    return pdf_files


if __name__ == "__main__":
    start_year = int(input("Start year: "))
    end_year = int(input("End year: "))
    api_endpoint = input("API ENDPOINT:  ")
    
    for year in range(start_year, end_year +1 ):
        year_directory = os.path.join(base_directory, str(year))
        if not os.path.exists(year_directory) or not os.path.isdir(year_directory):
            continue  # Skip if the directory doesn't exist

        pdf_files = find_pdfs(year_directory, year)
        total_files = len(pdf_files)
        
        for index, (file_path, file_link) in enumerate(pdf_files, start=1):
            if file_link in posted_filelink:
                print(f"Already Posted: {file_link}")
                continue

            payload = {
                "fileName": os.path.basename(file_path),
                "status": True,
                "fileLink": f"dirittopratico/{file_link}",
                "dateTime": (datetime.now() - timedelta(days=2)) .isoformat()
            }

            response = requests.post(f"{SERVER_URL}:{PORT}/{api_endpoint}", json=payload)
            if response.status_code == 200:
                with open("posted.txt", "a") as file:
                    file.write(f"{file_link}\n")
                print(f"[{year} ==> {index} / {total_files}] Successfully posted")
            else:
                print(f"[{year} ==> {index} / {total_files}] Failed to post: {response.status_code}")
