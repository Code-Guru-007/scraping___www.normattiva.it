from ftplib import FTP
import os


def UploadPdf():
    SERVER = "109.205.183.137"
    USERNAME = "normative@db-legale.professionista-ai.com"
    PASSWORD = "aoewiuyrfpqiu34jf209i3f4"
    download_dir = f'{os.getcwd()}\\download'
    session = FTP(SERVER, USERNAME, PASSWORD)

    for f in os.listdir(download_dir):
        print(f)
        files = FTP.nlst(session)  # List the files in the current directory
        if f in files:
            print(f"{f} exists on the server.")
        else:
            file = open(f'{download_dir}\\{f}', 'rb')
            session.storbinary(f'STOR {f}', file)     # send the file
            file.close()                                    # close file and FTP
    session.quit()