from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
import time
import os
import re
from selenium.webdriver.chrome.options import Options




def ScrapeList(start = 2010, end = 2010):
    baseUrl = "https://www.normattiva.it/ricerca/elencoPerData"
    data = []
    download_dir = f'{os.getcwd()}\\download'
    
    chrome_options = Options()
    chrome_options.add_experimental_option('prefs',  {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
        }
    )

    driver = webdriver.Chrome(options = chrome_options)
    
    for year in range(start, end + 1, 1):
        print("Current Year :    ", year)
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
                            match = re.search(r'n\.\s*(\d+)', content)
                            if match:
                                number = match.group(1)  # Extract the matched number
                                print(number)
                            parsed_url = urlparse(href)
                            query_params = parse_qs(parsed_url.query)
                            date = query_params.get('atto.dataPubblicazioneGazzetta', [None])[0]
                            code = query_params.get('atto.codiceRedazionale', [None])[0]
                            # check if current file has been downloaded
                            download_dir = f'{os.getcwd()}\\download'
                            pdf_files = [file for file in os.listdir(download_dir) if file.endswith('.pdf')]
                            match = any(file.startswith(f'{number}_{year}') for file in pdf_files)
                            if match:
                                print(f'{number}_{year}')
                                continue
                            
                            card[i].find_element(By.CSS_SELECTOR, 'p > a').click()
                            driver.get(f'https://www.normattiva.it/atto/vediMenuExport?atto.dataPubblicazioneGazzetta={date}&atto.codiceRedazionale={code}&currentSearch=')
                            pdf_button = driver.find_element(By.NAME, 'downloadPdf')
                            pdf_button.click()
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
        except:
            pass

    driver.close()    

ScrapeList()