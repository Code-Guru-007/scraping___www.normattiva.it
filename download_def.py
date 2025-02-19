import requests
from lxml import etree
import urllib.parse
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import re
from selenium.webdriver.chrome.options import Options
from ftplib import FTP
import glob
import datetime

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

# source_lists = ["normativaLink", "prassiLink", "giurisprudenzaLink"]
source_lists = [ "prassiLink", "giurisprudenzaLink"]

SERVER_URL = os.getenv("SERVER_URL", "http://188.245.216.211")


for source in source_lists:
    downloaded_list = []
    download_dir = os.path.join(os.getcwd(), source)
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
    
    with open(f"{source}.txt", 'r') as f:
        ids = [line.strip() for line in f.readlines()]
    if os.path.exists('downloaded.txt'):
        with open('downloaded.txt', 'r') as file:
            downloaded_list = [line.strip() for line in file.readlines()]
    
    for id in ids:
        if id in downloaded_list:
            print("Already downloaded!")
            continue
        if source == "normativaLink":
            url = f"https://def.finanze.it/DocTribFrontend/executeCallFromMenu.do?actionParam=visualizza/stampa%20atto%20in%20pdf&idAttoCorrente={id}&TIPO_CITATI=ATTO_NORMATIVO"
        if source == "prassiLink":
            url = f"https://def.finanze.it/DocTribFrontend/getPrassiDetail.do?id={id}"
        if source == "giurisprudenzaLink":
            url = f"https://def.finanze.it/DocTribFrontend/getGiurisprudenzaDetail.do?id={id}"
        driver.get(url)
        try:
            if source == "normativaLink":
                submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            if source == "prassiLink":
                submit_button = driver.find_element(By.ID, "stampaPrassi")
            if source == "giurisprudenzaLink":
                submit_button = driver.find_element(By.ID, "stampaGiurisprudenza")
            submit_button.click()
            time.sleep(3)
            
            pdf_files = [f for f in os.listdir(download_dir) if f.endswith(".pdf")]
            # Get the most recently modified PDF file
            if pdf_files:
                latest_pdf = max(
                    (os.path.join(download_dir, f) for f in pdf_files), 
                    key=os.path.getmtime
                )
                filename = os.path.basename(latest_pdf)
                print("Last downloaded PDF file:", filename)
            else:
                print("No PDF files found in the directory.")
            
            
            requests.post(f"{SERVER_URL}:8000/api/def.finanze.it", json={
                "fileName": filename,
                "status": True,
                "fileLink": f"{SERVER_URL}/public/download/normattiva_local/{os.getcwd().split('\\')[-1]}/{source}/{filename}",
                "dateTime": datetime.datetime.now().isoformat()
            })
            with open('downloaded.txt', 'a') as file:
                file.write(f'{id}\n')
            
            print("filename:", filename)
        except Exception as e:
            print("Exception occur! >>   ", e)
            
    driver.quit()