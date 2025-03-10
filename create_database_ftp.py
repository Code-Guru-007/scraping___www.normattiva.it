import os
import datetime
import requests
import ftplib

# FTP Config
FTP_HOST = "109.205.183.137"
FTP_USER = "legal_doc@db-legale.professionista-ai.com"
FTP_PASS = "G}SsFa@dB@&3"

# API Config
SERVER_URL = "http://188.245.216.211"
PORT = 8000  # Change if needed

# Read posted file links
posted_filelink = []
if os.path.exists("ftp_posted.txt"):
    with open("ftp_posted.txt", "r") as file:
        posted_filelink = [line.strip() for line in file.readlines()]


def list_ftp_pdfs(ftp, directory, year):
    """Recursively list PDF files in an FTP directory without downloading"""
    pdf_files = []
    
    try:
        ftp.cwd(directory)  # Change to target directory
        items = ftp.nlst()  # List files and directories

        for item in items:
            if item == "." or item == "..":
                continue
            full_path = f"{directory}/{item}"  # Ensure clean paths
            print(f"          {full_path}")
            try:
                ftp.cwd(full_path)  # Try entering directory
                ftp.cwd("..")  # If successful, it's a directory
                sub_pdfs = list_ftp_pdfs(ftp, full_path, year)
                pdf_files.extend(sub_pdfs)
            except ftplib.error_perm:
                # It's a file if we can't change directory
                if item.endswith(".pdf"):
                    relative_path = full_path.split(f"/{year}/")[-1]
                    file_link = f"{year}/{relative_path}"
                    if file_link in posted_filelink:
                        print(f"Already Posted: {file_link}")
                        continue

                    payload = {
                        "fileName": file_link.split("/")[-1],
                        "status": True,
                        "fileLink": f"dirittopratico/{file_link}",
                        "dateTime": datetime.datetime.now().isoformat()
                    }
                    

                    response = requests.post(f"{SERVER_URL}:{PORT}/{api_endpoint}", json=payload)

                    if response.status_code == 200:
                        with open("ftp_posted.txt", "a") as file:
                            file.write(f"{file_link}\n")
                        print(f"Successfully posted")
                    else:
                        print(f"Failed to post: {response.status_code}")
                    pdf_files.append((full_path, file_link))
    except ftplib.error_perm:
        print(f"Error accessing directory: {directory}")

    return pdf_files


if __name__ == "__main__":
    start_year = int(input("Start year: "))
    end_year = int(input("End year: "))
    api_endpoint = input("API ENDPOINT: ")

    with ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS) as ftp:
        # ftp.login()
        print("Connected to FTP server")

        for year in range(start_year, end_year + 1):
            year_directory = f"/sentenze_merito/downloaded/dirittopratico/{year}"  # Adjust based on FTP structure
            try:
                ftp.cwd(year_directory)  # Check if directory exists
            except ftplib.error_perm:
                print(f"Skipping {year}, directory not found")
                continue

            pdf_files = list_ftp_pdfs(ftp, year_directory, year)
            total_files = len(pdf_files)

            # for index, (remote_file, file_link) in enumerate(pdf_files, start=1):
            #     if file_link in posted_filelink:
            #         print(f"Already Posted: {file_link}")
            #         continue

            #     payload = {
            #         "fileName": os.path.basename(remote_file),
            #         "status": True,
            #         "fileLink": f"dirittopratico/{file_link}",
            #         "dateTime": datetime.datetime.now().isoformat()
            #     }
                
            #     print(payload)

                # response = requests.post(f"{SERVER_URL}:{PORT}/{api_endpoint}", json=payload)

                # if response.status_code == 200:
                #     with open("ftp_posted.txt", "a") as file:
                #         file.write(f"{file_link}\n")
                #     print(f"[{year} ==> {index} / {total_files}] Successfully posted")
                # else:
                #     print(f"[{year} ==> {index} / {total_files}] Failed to post: {response.status_code}")
