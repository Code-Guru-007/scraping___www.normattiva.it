from ftplib import FTP
import os


def upload_pdf(year):
    SERVER = "109.205.183.137"
    USERNAME = "legal_doc@db-legale.professionista-ai.com"
    PASSWORD = "G}SsFa@dB@&3"
    session = FTP(SERVER, USERNAME, PASSWORD)
    
    base_dir = f"/normative_locali/downloaded/{year}"
    download_dir = os.path.join(os.getcwd(), "download", "normattiva_local", year)
    with open(os.path.join(download_dir, "download_url.txt"), 'r') as file:
        filenames = [line.strip().split("./")[1].replace("/", "_") for line in file.readlines()]

    for filename in filenames:
        sub_path = os.path.join(download_dir, filename.split('_')[0])
        remote_sub_path = f"{base_dir}/{filename.split('_')[0]}"
        
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
        
        for f in os.listdir(sub_path):
            files = session.nlst()
            print(f)
            if f in files:
                print(f"{f} exists on the server.")
            else:
                try:
                    with open(os.path.join(sub_path, f), 'rb') as file:
                        session.storbinary(f'STOR {f}', file)
                except:
                    print(f"Error occurred while uploading: {f}")
    
    session.quit()