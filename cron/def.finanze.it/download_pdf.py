import os
import time
import shutil
import requests
import datetime
from ftplib import FTP
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

FTP_SERVER = "109.205.183.137"
FTP_USERNAME = "legal_doc@db-legale.professionista-ai.com"
FTP_PASSWORD = "G}SsFa@dB@&3"


source_lists = ["Normativa", "Prassi", "Giurisprudenza"]

SERVER_URL = os.getenv("SERVER_URL", "http://188.245.216.211")

def download_pdf(base_dir, year):
    print(base_dir, year)
    global source_lists
    for source in source_lists:
        downloaded_list = []
        print(source)
        download_dir = os.path.join(base_dir, source)
        os.makedirs(download_dir, exist_ok=True)
        #################################
        ##### Selenium Setting   #####
        #################################
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--user-data-dir=/tmp/chrome_profile")
        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        })
        
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        ###################################
        ###################################
        ids = []
        count = 0
        if os.path.exists(os.path.join(base_dir, f"{source.lower()}Link.txt")):
            with open(os.path.join(base_dir, f"{source.lower()}Link.txt"), 'r') as f:
                ids = [line.strip() for line in f.readlines()]
        if os.path.exists(os.path.join(base_dir,'downloaded.txt')):
            with open(os.path.join(base_dir,'downloaded.txt'), 'r') as file:
                downloaded_list = [line.strip() for line in file.readlines()]
        
        for id in ids:
            count += 1
            if id in downloaded_list:
                print(f"[{count}/{len(ids)}]     >>>>>     Already downloaded!")
                continue
            if source == "Normativa":
                url = f"https://def.finanze.it/DocTribFrontend/executeCallFromMenu.do?actionParam=visualizza/stampa%20atto%20in%20pdf&idAttoCorrente={id}&TIPO_CITATI=ATTO_NORMATIVO"
            if source == "Prassi":
                url = f"https://def.finanze.it/DocTribFrontend/getPrassiDetail.do?id={id}"
            if source == "Giurisprudenza":
                url = f"https://def.finanze.it/DocTribFrontend/getGiurisprudenzaDetail.do?id={id}"
            driver.get(url)
            try:
                if source == "Normativa":
                    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                if source == "Prassi":
                    submit_button = driver.find_element(By.ID, "stampaPrassi")
                if source == "Giurisprudenza":
                    submit_button = driver.find_element(By.ID, "stampaGiurisprudenza")
                submit_button.click()
                time.sleep(5)
                error = driver.find_element(By.TAG_NAME, "body").text
                if error.startswith('Error 500'):
                    print(f"[{count}/{len(ids)}]     >>>>>     Error 500")
                    requests.post(f"{SERVER_URL}:8000/api/def.finanze.it", json={
                        "fileName": id,
                        "status": False,
                        "fileLink": "",
                        "dateTime": datetime.datetime.now().isoformat()
                    })
                    with open(os.path.join(base_dir,'downloaded.txt'), 'a') as file:
                        file.write(f'{id}\n')
                    continue
                pdf_files = [f for f in os.listdir(download_dir) if f.endswith(".pdf")]
                # Get the most recently modified PDF file
                if pdf_files:
                    latest_pdf = max(
                        (os.path.join(download_dir, f) for f in pdf_files), 
                        key=os.path.getmtime
                    )
                    filename = os.path.basename(latest_pdf)
                else:
                    print("     No PDF files found in the directory.")
                    
                upload_file(download_dir, filename, source, year)
                copy_file_to_www(download_dir, filename, source, year)
                
                requests.post(f"{SERVER_URL}:8000/api/def.finanze.it", json={
                    "fileName": filename,
                    "status": True,
                    "fileLink": f"{source}/{year}/{filename}",
                    "dateTime": datetime.datetime.now().isoformat()
                })
                with open(os.path.join(base_dir,'downloaded.txt'), 'a') as file:
                    file.write(f'{id}\n')
                
                print(f"[{count}/{len(ids)}]     >>>>>     Downloaded")
            except Exception as e:
                print(f"[{count}/{len(ids)}]     >>>>>     Exception occur!\n", e)
                
        driver.quit()

def upload_file(directory, filename, year, source):
    """Uploads the file to an FTP server."""
    session = FTP(FTP_SERVER, FTP_USERNAME, FTP_PASSWORD)
    upload_dir = f'/fisco/downloaded/def.finanze.it/{source}'
    session.cwd(upload_dir)
    if str(year) not in session.nlst():
        session.mkd(f'{year}')
    session.cwd(f'{upload_dir}/{year}')
    
    if filename not in session.nlst():
        try:
            with open(os.path.join(directory, filename), 'rb') as file:
                session.storbinary(f'STOR {filename}', file)
            print(f"     Uploaded: {filename}")
        except Exception as e:
            print(f"     Upload failed: {e}")
    else:
        print(f"     File already exists on server: {filename}")
    session.quit()
    
def copy_file_to_www(directory, filename, year, source):
    """Copies the file to the web-accessible directory."""
    target_dir = f"/var/www/html/public/download/def.finanze.it/{source}/{year}"
    os.makedirs(target_dir, exist_ok=True)
    shutil.copy(os.path.join(directory, filename), os.path.join(target_dir, filename))
    print(f"     File copied to: {target_dir}/{filename}")


download_pdf("/root/test/def.finanze.it/download/def.finanze.it/2025", 2025)
