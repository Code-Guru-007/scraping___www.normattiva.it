import os
import time
import shutil
import requests
import datetime
from ftplib import FTP
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

FTP_SERVER = "109.205.183.137"
FTP_USERNAME = "normative@db-legale.professionista-ai.com"
FTP_PASSWORD = "aoewiuyrfpqiu34jf209i3f4"
SERVER_URL = os.getenv("SERVER_URL", "http://188.245.216.211")

# proxy_username = "dBmTABWe6lHt7Lzi"
# proxy_password = "7hsc7iCVnOMLTmGO"
# proxy_address = "geo.iproyal.com"
# proxy_port = "12321"
proxy_username = "c7fjetgtletu"
proxy_password = "JXTWkrkRsUQFsVcb"
proxy_address = "104.234.48.92"
proxy_port = "6010"

proxy_url = f"http://{proxy_username}:{proxy_password}@{proxy_address}:{proxy_port}"

proxy = {
    "http": proxy_url,
    "https": proxy_url
}

proxy_url = f"http://{proxy_username}:{proxy_password}@{proxy_address}:{proxy_port}"

seleniumwire_options = {
    "proxy": proxy
}

source_lists = ["Normativa", "Prassi", "Giurisprudenza"]


def download_pdf(base_dir, year):
    for source in source_lists:
        downloaded_list = []
        download_dir = os.path.join(base_dir, source)
        os.makedirs(download_dir, exist_ok=True)
        #################################
        ##### Selenium Setting   #####
        #################################
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--remote-debugging-port=9222")  # Debugging port
        # chrome_options.add_argument("--user-data-dir=/tmp/chrome_profile")
        chrome_options.add_experimental_option('prefs',  {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
            }
        )
        # options.add_argument("--headless=new")  # Uncomment if you want headless mode

        # Start the WebDriver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            seleniumwire_options=seleniumwire_options,
            options=chrome_options
        )
        ###################################
        ###################################
        ids = []
        count = 0
        if os.path.exists(f"{source.lower()}Link.txt"):
            with open(f"{source.lower()}Link.txt", 'r') as f:
                ids = [line.strip() for line in f.readlines()]
        if os.path.exists('downloaded.txt'):
            with open('downloaded.txt', 'r') as file:
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
                    with open('downloaded.txt', 'a') as file:
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
                    "fileLink": f"{source}/{os.getcwd().split('\\')[-1]}/{filename}",
                    "dateTime": datetime.datetime.now().isoformat()
                })
                with open('downloaded.txt', 'a') as file:
                    file.write(f'{id}\n')
                
                print(f"[{count}/{len(ids)}]     >>>>>     Downloaded")
            except Exception as e:
                print(f"[{count}/{len(ids)}]     >>>>>     Exception occur!\n", e)
                
        driver.quit()

def upload_file(directory,filename, year, source):
    """Uploads the file to an FTP server."""
    session = FTP(FTP_SERVER, FTP_USERNAME, FTP_PASSWORD)
    base_dir = f'/fisco/downloaded/def.finanze.it/{source}'
    session.cwd(base_dir)
    if year not in session.nlst():
        session.mkd(f'{year}')
    session.cwd(f'{base_dir}/{year}')
    
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

