from ftplib import FTP
import os


def UploadPdf():
    SERVER = "109.205.183.137"
    USERNAME = "normative@db-legale.professionista-ai.com"
    PASSWORD = "aoewiuyrfpqiu34jf209i3f4"
    download_dir = f'{os.getcwd()}\\download'
    session = FTP(SERVER, USERNAME, PASSWORD)
    directories = FTP.nlst(session) 
    if "ftp" in directories:
        FTP.cwd(session, '/ftp')
        files = FTP.nlst(session)
    else:
        FTP.mkd(session, 'ftp')
        FTP.cwd(session, '/ftp')
        files = FTP.nlst(session)

    for f in os.listdir(download_dir):
        print(f)
        if f in files:
            print(f"{f} exists on the server.")
        else:
            try:
                file = open(f'{download_dir}\\{f}', 'rb')
                session.storbinary(f'STOR {f}', file)     # send the file
                file.close()                                    # close file and FTP
            except:
                print(f"Error occur!   :   {f}")
    session.quit()
    
UploadPdf()