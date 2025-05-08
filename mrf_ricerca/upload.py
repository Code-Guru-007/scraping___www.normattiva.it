from ftplib import FTP
import os


def UploadPdf(year):
    SERVER = "109.205.183.137"
    USERNAME = "normative@db-legale.professionista-ai.com"
    PASSWORD = "aoewiuyrfpqiu34jf209i3f4"
    download_dir = f'{os.getcwd()}/download/{year}'
    session = FTP(SERVER, USERNAME, PASSWORD)

    for f in os.listdir(download_dir):
        FTP.cwd(session, '/')
        directories = FTP.nlst(session) 
        year = f.split(".")[0].split("_")[-1]
        if year in directories:
            FTP.cwd(session, f'/{year}')
            files = FTP.nlst(session)
        else:
            FTP.mkd(session, year)
            FTP.cwd(session, f'/{year}')
        files = FTP.nlst(session)
        print(f)
        if f in files:
            print(f"{f} exists on the server.")
        else:
            try:
                file = open(f'{download_dir}/{f}', 'rb')
                session.storbinary(f'STOR {f}', file)     # send the file
                file.close()                                    # close file and FTP
            except:
                print(f"Error occur!   :   {f}")
    session.quit()