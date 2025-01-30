from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
import time
import os
import re
from selenium.webdriver.chrome.options import Options




def ScrapeList(start, end):
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
                            parsed_url = urlparse(href)
                            query_params = parse_qs(parsed_url.query)
                            date = query_params.get('atto.dataPubblicazioneGazzetta', [None])[0]
                            code = query_params.get('atto.codiceRedazionale', [None])[0]
                            output = extract_filename(content)
                            filename = f"{output['title']}_{year}"
                            download_dir = f'{os.getcwd()}\\download'
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
                            time.sleep(3)
                            try:
                                new_name = f"{filename}.pdf"
                                old_path1 = f'{output['number']}_{year} (1).pdf'
                                old_path2 = f'{output['number']}_{year}.pdf'
                                rename_file(download_dir, old_path1, old_path2, new_name)
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
        except:
            pass
    driver.close()    


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
        print("No file found to rename.")    