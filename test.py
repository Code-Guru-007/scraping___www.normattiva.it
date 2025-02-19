from ftplib import FTP
import re

# FTP Credentials
FTP_HOST = "109.205.183.137"
FTP_USER = "legal_doc@db-legale.professionista-ai.com"
FTP_PASS = "G}SsFa@dB@&3"

# Connect to FTP server
ftp = FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)

# Change to the target directory (if necessary)
ftp.cwd('/sentenze_cassazione/downloaded/2025')  # Modify as needed

# List all directories
directories = ftp.nlst()  # Fetch all directory names

# Regular expression to match directories in YYYYMMDD format
pattern = re.compile(r"^(\d{4})(\d{2})(\d{2})$")

for dirname in directories:
    match = pattern.match(dirname)
    if match:
        # Extract YYYY, MM, DD
        yyyy, mm, dd = match.groups()
        new_name = f"{yyyy}-{mm}-{dd}"  # Format as YYYY-MM-DD

        # Rename the directory
        try:
            ftp.rename(dirname, new_name)
            print(f"Renamed: {dirname} -> {new_name}")
        except Exception as e:
            print(f"Failed to rename {dirname}: {e}")

# Close FTP connection
ftp.quit()
