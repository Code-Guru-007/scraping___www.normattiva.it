from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
import time
import os
import re
from selenium.webdriver.chrome.options import Options
from ftplib import FTP
import datetime
import upload

SERVER = "109.205.183.137"
USERNAME = "normative@db-legale.professionista-ai.com"
PASSWORD = "aoewiuyrfpqiu34jf209i3f4"
session = FTP(SERVER, USERNAME, PASSWORD)

error_list = []


def ScrapeList(year):
    print("Current Year :    ", year)
    baseUrl = "https://www.normattiva.it/ricerca/elencoPerData"
    download_dir = f'{os.getcwd()}\\download\\{year}'
    
    chrome_options = Options()
    chrome_options.add_experimental_option('prefs',  {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
        }
    )

    driver = webdriver.Chrome(options = chrome_options)
    try:
        driver.get(f'{baseUrl}/anno/{year}')
        current_page = 0
        driver.get(f'{baseUrl}/{current_page}')
        card = driver.find_elements(By.XPATH, "//div[starts-with(@id, 'heading_')]")
        while len(card):
            try:
                for i in range(len(card)):
                    try:
                        href = card[i].find_element(By.CSS_SELECTOR, 'p > a').get_attribute("href")    
                        content = card[i].find_element(By.CSS_SELECTOR, 'p > a').get_attribute("innerHTML")
                        parsed_url = urlparse(href)
                        query_params = parse_qs(parsed_url.query)
                        date = query_params.get('atto.dataPubblicazioneGazzetta', [None])[0]
                        code = query_params.get('atto.codiceRedazionale', [None])[0]
                        output = extract_filename(content)
                        filename = f"{output['title']}_{year}"
                        pdf_files = [file for file in os.listdir(download_dir) if file.endswith('.pdf')]

                        match = any(file.startswith(filename) for file in pdf_files)
                        if match:
                            print("Already Downloaded :  ", filename)
                            continue
                        print(filename)
                        card[i].find_element(By.CSS_SELECTOR, 'p > a').click()
                        driver.get(f'https://www.normattiva.it/atto/vediMenuExport?atto.dataPubblicazioneGazzetta={date}&atto.codiceRedazionale={code}&currentSearch=')
                        pdf_button = driver.find_element(By.NAME, 'downloadPdf')
                        pdf_button.click()
                        time.sleep(5)
                        try:
                            new_name = f"{filename}.pdf"
                            old_path1 = f'{output['number']}_{year} (1).pdf'
                            old_path2 = f'{output['number']}_{year}.pdf'
                            rename_file(download_dir, old_path1, old_path2, new_name)
                            upload_file(download_dir, new_name)
                        except:
                            print("----------------")
                            pass
                        
                        driver.switch_to.window(driver.window_handles[0])
                        driver.back()
                        driver.back()
                        card = driver.find_elements(By.XPATH, "//div[starts-with(@id, 'heading_')]")
                    except:
                        pass
                current_page += 1
                driver.get(f'{baseUrl}/{current_page}')
                card = driver.find_elements(By.XPATH, "//div[starts-with(@id, 'heading_')]")
            except:
                pass
        global error_list
        print(error_list)
        for item in error_list:
            rename_file(item['directory'], item['original_name1'], item['original_name2'], item['new_name'])
            upload_file(item['directory'], item['new_name'])
    except:
        pass
    driver.close()    

def upload_file(download_dir, filename):
    global session
    FTP.cwd(session, '/')
    directories = FTP.nlst(session) 
    year = filename.split(".")[0].split("_")[-1]
    if f'test-{year}' in directories:
        FTP.cwd(session, f'/test-{year}')
        files = FTP.nlst(session)
    else:
        FTP.mkd(session, f'test-{year}')
        FTP.cwd(session, f'/test-{year}')
    files = FTP.nlst(session)
    print(filename)
    if filename in files:
        print(f"{filename} exists on the server.")
    else:
        try:
            file = open(f'{download_dir}\\{filename}', 'rb')
            session.storbinary(f'STOR {filename}', file)     # send the file
            file.close()                                    # close file and FTP
        except:
            print(f"Error occur!   :   {filename}")


def extract_filename(text):
    number_match = re.search(r"\((\d+)\)", text)
    number = number_match.group(1) if number_match else None
    title_match = re.search(r"n\.\s*(\d+)?\s*([\w]+)?", text.strip(), re.MULTILINE)
    if title_match:
        num_part = title_match.group(1)  # The numeric part
        word_part = title_match.group(2)  # The additional text (Roman numeral or descriptor)

        if word_part and number:
            return {
                'title': f"{word_part}_{number}",
                'number': number
            }  # Case: "DXXIX_529" or "novies_408"
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
            
def rename_file(directory, original_name1, original_name2, new_name):
    file1 = os.path.join(directory, original_name1)
    file2 = os.path.join(directory, original_name2)
    new_file_path = os.path.join(directory, new_name)

    if os.path.exists(file1):
        os.rename(file1, new_file_path)
        print(f"Renamed: {original_name1} → {new_name}")
    elif os.path.exists(file2):
        os.rename(file2, new_file_path)
        print(f"Renamed: {original_name2} → {new_name}")
    else:
        global error_list
        error_list.append({
            'directory': directory,
            'original_name1' : original_name1,
            'original_name2' : original_name2,
            'new_name': new_name
            })
        print("No file found to rename.")    