from ftplib import FTP
import os

def upload_pdf(year):
    SERVER = "109.205.183.137"
    USERNAME = "legal_doc@db-legale.professionista-ai.com"
    PASSWORD = "G}SsFa@dB@&3"
    
    session = FTP(SERVER)
    session.login(USERNAME, PASSWORD)
    
    base_dir = f"/sentenze_cassazione/downloaded/{year}"
    local_year_dir = os.getcwd()
    
    def upload_directory(local_dir, remote_dir):
        try:
            session.cwd(remote_dir)
        except:
            print(f"Creating directory: {remote_dir}")
            parts = remote_dir.split('/')
            current_path = ''
            for part in parts:
                if part:
                    current_path += f'/{part}'
                    try:
                        session.cwd(current_path)
                    except:
                        session.mkd(current_path)
                        session.cwd(current_path)
        
        for item in os.listdir(local_dir):
            local_path = os.path.join(local_dir, item)
            remote_path = f"{remote_dir}/{item}"
            
            if os.path.isdir(local_path):
                upload_directory(local_path, remote_path)
            elif item.lower().endswith('.pdf'):
                if item in session.nlst():
                    print(f"{item} already exists on the server.")
                else:
                    try:
                        with open(local_path, 'rb') as file:
                            session.storbinary(f'STOR {item}', file)
                        print(f"Uploaded: {item}")
                    except Exception as e:
                        print(f"Error uploading {item}: {e}")
    
    upload_directory(local_year_dir, base_dir)
    session.quit()
    print("Upload completed!")

# Example usage:
upload_pdf(2025)