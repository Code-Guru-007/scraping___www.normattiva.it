from seleniumbase import Driver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.print_page_options import PrintOptions
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse, parse_qs
import pyautogui
import time
import os

baseUrl = "https://www.normattiva.it/ricerca/elencoPerData"
data = []
download_dir = f'{os.getcwd()}\\download'
driver = Driver(uc=True)


def ScrapeList(start = 2010, end = 2015):
    for year in range(start, end, 1):
        driver.get(f'{baseUrl}/anno/{year}')
        current_page = 0
        driver.get(f'{baseUrl}/{current_page}')
        
        card = driver.find_elements(By.XPATH, "//div[starts-with(@id, 'heading_')]")
        # while len(card):
        while current_page < 2:
            # for i in range(len(card)):
            for i in range(1):           
                href = card[i].find_element(By.CSS_SELECTOR, 'p > a').get_attribute("href")            
                parsed_url = urlparse(href)
                query_params = parse_qs(parsed_url.query)
                date = query_params.get('atto.dataPubblicazioneGazzetta', [None])[0]
                
                #check if current file has been downloaded
                download_dir = f'{os.getcwd()}\\download'
                pdf_files = [file for file in os.listdir(download_dir) if file.endswith('.pdf')]
                match = any(file.startswith(date) for file in pdf_files)
                if match:
                    print(date)
                    continue
                
                code = query_params.get('atto.codiceRedazionale', [None])[0]
                card[i].find_element(By.CSS_SELECTOR, 'p > a').click()
                driver.get(f'https://www.normattiva.it/atto/vediMenuExport?atto.dataPubblicazioneGazzetta={date}&atto.codiceRedazionale={code}&currentSearch=')
                pdf_button = driver.find_element(By.NAME, 'downloadPdf')
                pdf_button.click()
                driver.switch_to.window(driver.window_handles[1])
                element = driver.find_element(By.TAG_NAME, 'body')
                action = ActionChains(driver)
                action.move_to_element(element).click().perform()
                
                pyautogui.hotkey('ctrl', 's')
                time.sleep(1)
                pyautogui.write(f'{download_dir}\\{date}.pdf')
                time.sleep(1)
                pyautogui.hotkey('enter')
                time.sleep(1)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.back()
                driver.back()
            current_page += 1
            driver.get(f'{baseUrl}/{current_page}')
            time.sleep(2)
            card = driver.find_elements(By.XPATH, "//div[starts-with(@id, 'heading_')]")
        time.sleep(1)

    driver.close()    

# ScrapeList()