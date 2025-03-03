import os
import time
import datetime
import requests
from ftplib import FTP
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FTP_SERVER = "109.205.183.137"
FTP_USERNAME = "legal_doc@db-legale.professionista-ai.com"
FTP_PASSWORD = "G}SsFa@dB@&3"
SERVER_URL = os.getenv("SERVER_URL", "http://188.245.216.211")

def download_pdf(year):
    download_dir = os.path.join(os.getcwd(), "download", "ilmerito.it", str(year))
    os.makedirs(download_dir, exist_ok=True)
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--remote-debugging-port=9222")
    # chrome_options.add_argument("--user-data-dir=/tmp/chrome_profile")
    chrome_options.add_experimental_option('prefs', {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })
    
    # service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.ilmerito.it/")
    uname = driver.find_element(By.XPATH, "//input[@name='uname']")
    uname.clear()
    uname.send_keys("studiosorrentino@legalmail.it")
    pwd = driver.find_element(By.XPATH, "//input[@name='pwd']")
    pwd.clear()
    pwd.send_keys("dolqbnfqal")
    submit = driver.find_element(By.XPATH, "//input[@type='submit']")
    submit.click()
    time.sleep(3)
    with open(os.path.join(download_dir, "buf.txt"), 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    total = len(urls)
    current = 0
    for url in urls:
        try:
            current += 1
            driver.get(url)
            try:
                a_tag = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//font[@class='black12']/a"))
                )
                driver.execute_script("arguments[0].click();", a_tag)  # Use JS click
                time.sleep(60)
            except Exception as e:
                print(f"Error clicking link: {e}")
                continue
            
            time.sleep(2)
            error = "Errore! Contenuto non disponibile."
            body_text = driver.find_element(By.TAG_NAME, "body").text
            with open(os.path.join(download_dir, 'pdf_urls.txt'), "a") as file:
                file.write(f"{url}\n")
                
            if body_text == error:
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
            if filename:
                upload_file(download_dir, filename, year)
                # payload = {
                #     "fileName": filename,
                #     "status": True,
                #     "fileLink": f"{year}/{filename}",
                #     "dateTime": datetime.datetime.now().isoformat()
                # }

                # requests.post(f"{SERVER_URL}:8000/api/ilmerito.it", json=payload)
        except Exception as e:
            print(e)
            with open(os.path.join(download_dir, "failed.txt"), "a") as file:
                file.write(f"{url}\n")
    driver.quit()
    
    if(os.path.exists(os.path.join(download_dir, "buf.txt"))):
        os.remove(os.path.join(download_dir, "buf.txt"))
                
def upload_file(directory,filename, year):
    """Uploads the file to an FTP server."""
    session = FTP(FTP_SERVER, FTP_USERNAME, FTP_PASSWORD)
    base_dir = f'/sentenze_merito/downloaded'
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
    
download_pdf(2025)