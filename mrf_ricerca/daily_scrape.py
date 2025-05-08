import os
import re
import time
import shutil
import datetime
import requests
from ftplib import FTP
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse, parse_qs

# Configurable Settings
FTP_SERVER = os.getenv("FTP_SERVER", "109.205.183.137")
FTP_USERNAME = os.getenv("FTP_USERNAME", "legal_doc@db-legale.professionista-ai.com")
FTP_PASSWORD = os.getenv("FTP_PASSWORD", "G}SsFa@dB@&3")
SERVER_URL = os.getenv("SERVER_URL", "http://188.245.216.211")

def ScrapeList(year):
    """Scrapes PDFs from Normattiva and downloads them."""
    base_url = "https://www.normattiva.it/mfr/ricerca/semplice"
    download_dir = f'{os.getcwd()}/download/normative/{year}'
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
    # driver = webdriver.Chrome(service=service, options=chrome_options)
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://www.normattiva.it/mfr/ricerca/semplice?back=true")
        # driver.get(f'{base_url}/anno/{year}')
        print(f"Scraping year: {year}")
        year_input = driver.find_element(By.ID, "annoProvvedimento")
        year_input.clear()
        year_input.send_keys(str(year))

        search_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        search_btn.click()

        time.sleep(2)

        driver.get("https://www.normattiva.it/mfr/ricerca/semplice/filter/add/tipoTestoCod/VIGENTE")

        page = 1
        driver.get(f'{base_url}/{page}')
        elements = driver.find_elements(By.CSS_SELECTOR, "a.d-block.font-weight-semibold")
        while len(elements):
            try:
                for i in range(len(elements)):
                    try:
                        with open(f"{year}.txt", "a") as file:
                            print(elements[i].get_attribute("href"))
                            file.write(f"{elements[i].get_attribute("href")}\n")

                    except Exception as e:
                        print(f"Skipping entry due to error: {e}")

                page += 1
                driver.get(f'{base_url}/{page}')
                elements = driver.find_elements(By.CSS_SELECTOR, "a.d-block.font-weight-semibold")
                time.sleep(1)
            except Exception as e:
                print(f"Error on page {page}: {e}")
                break

    finally:
        driver.quit()

# def extract_filename(text):
#     """Extracts document number and title from text."""
#     match = re.search(r"n\.\s*(\d+)\s*([\w]*)?", text.strip())
#     if match:
#         number, word = match.groups()
#         title = f"{word}_{number}" if word else number
#         return {"title": title, "number": number}
#     return {"title": "Unknown", "number": "000"}

def extract_filename(text):
    number_match = re.search(r"\((\d+)\)", text)
    number = number_match.group(1) if number_match else None
    title_match = re.search(r"n\.\s*(\d+)?\s*([\w]+)?\s*(?:\(([^)]+)\))?", text.strip(), re.MULTILINE)

    if title_match:
        num_part = title_match.group(1)  # The numeric part (e.g., 1 or 408)
        word_part = title_match.group(2)  # The descriptor (e.g., "ter", "bis")
        descriptor_part = title_match.group(3)  # The content inside parentheses (e.g., "Raccolta 2025")
        if num_part and word_part:
            return {
                'title': f"{num_part}_{word_part}",
                'number': num_part
            }  # Case: "408_ter"
        elif num_part and descriptor_part:
            return {
                'title': f"{num_part}_{descriptor_part.replace(' ', '_')}",
                'number': num_part
            }  # Case: "1_Raccolta_2025"
        elif num_part:
            return {
                'title': num_part,
                'number': num_part
            }  # Case: "406"
        elif number:
            return {
                'title': number,
                'number': number
            }

def rename_file(directory, original_number, new_name, year):
    """Renames the downloaded file."""
    for suffix in [" (1)", ""]:
        old_path = os.path.join(directory, f"{original_number}_{year}{suffix}.pdf")
        if os.path.exists(old_path):
            new_path = os.path.join(directory, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed: {old_path} â†’ {new_path}")
            return True
    print("File not found to rename.")
    return False

def upload_file(directory, filename):
    """Uploads the file to an FTP server."""
    session = FTP(FTP_SERVER, FTP_USERNAME, FTP_PASSWORD)
    year = filename.split("_")[-1].split(".")[0]
    base_dir = '/normative/downloaded'
    session.cwd(base_dir)
    if year not in session.nlst():
        session.mkd(f'{year}')
    session.cwd(f'{base_dir}/{year}')
    
    if filename not in session.nlst():
        try:
            with open(os.path.join(directory, filename), 'rb') as file:
                session.storbinary(f'STOR {filename}', file)
            print(f"Uploaded: {filename}")
        except Exception as e:
            print(f"Upload failed: {e}")
    else:
        print(f"File already exists on server: {filename}")
    session.quit()
        

def copy_file_to_www(directory, filename, year):
    """Copies the file to the web-accessible directory."""
    target_dir = f"/var/www/html/public/download/normative/{year}"
    os.makedirs(target_dir, exist_ok=True)
    shutil.copy(os.path.join(directory, filename), os.path.join(target_dir, filename))
    print(f"File copied to: {target_dir}/{filename}")
