import os
import shutil
from ftplib import FTP


def upload_pdf(year):
    SERVER = "109.205.183.137"
    USERNAME = "legal_doc@db-legale.professionista-ai.com"
    PASSWORD = "G}SsFa@dB@&3"
    session = FTP(SERVER, USERNAME, PASSWORD)
    
    base_dir = f"/sentenze_cassazione/downloaded/{year}"
    download_dir = os.path.join(os.getcwd(), "download", "sentenze_cassazione", str(year))
    with open(os.path.join(download_dir, "download_url.txt"), 'r') as file:
        filenames = [line.strip().split("./")[1].replace("/", "_") for line in file.readlines()]

    for filename in filenames:
        date = filename.split('_')[0]
        sub_path = os.path.join(download_dir, date)
        remote_sub_path = f"{base_dir}/{date[:4]}-{date[4:6]}-{date[6:]}"
        try:
            session.cwd(remote_sub_path)
        except:
            print(f"Creating directory: {remote_sub_path}")
            parts = remote_sub_path.split('/')
            current_path = ''
            for part in parts:
                current_path += f'/{part}'
                try:
                    session.cwd(current_path)
                except:
                    session.mkd(current_path)
                    session.cwd(current_path)
        files = session.nlst()
        print(filename)
        if filename in files:
            print(f"{filename} exists on the server.")
        else:
            try:
                with open(os.path.join(sub_path, filename), 'rb') as file:
                    session.storbinary(f'STOR {filename}', file)
            except:
                print(f"Error occurred while uploading: {filename}")
        copy_file_to_www(os.path.join(download_dir, date), filename, year, date)
    session.quit()
    
    if(os.path.exists(os.path.join(download_dir, "download_url.txt"))):
        os.remove(os.path.join(download_dir, "download_url.txt"))
    print("\n\n")
def copy_file_to_www(directory, filename, year, date):
    """Copies the file to the web-accessible directory."""
    target_dir = f"/var/www/html/public/download/sentenze_cassazione/{year}/{date[:4]}-{date[4:6]}-{date[6:]}"
    os.makedirs(target_dir, exist_ok=True)
    shutil.copy(os.path.join(directory, filename), os.path.join(target_dir, filename))
    print(f"File copied to: {target_dir}/{filename}")