from seleniumbase import Driver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urlparse, parse_qs
import time
import os
import re

def ScrapeList():
    baseUrl = "https://www.italgiure.giustizia.it/sncass/"

    download_dir = f'{os.getcwd()}\\download\\www.italgiure.giustizia.it'
    print(">>>>>>>>>>>>>>>>>>    ", download_dir)
    # service = Service("/usr/bin/chromedriver")

    driver = driver = Driver(uc=True)
    # try:
    driver.get(baseUrl)
    wait = WebDriverWait(driver, 10)
    time.sleep(2)
    for i in range(1, 6):
        year = driver.find_element(By.ID, f"{i}.[anno]")
        year.click()
        time.sleep(2)
        next_page = driver.find_element(By.CLASS_NAME, "flipRight")
        while next_page.value_of_css_property("display") != "none":
            # pdf_elements = driver.find_elements(By.CLASS_NAME, "text2pdf")
            pdf_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "text2pdf")))

            for pdf_element in pdf_elements:
                try:
                    # Scroll element into view
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pdf_element)
                    time.sleep(0.5)  # Small delay to allow page adjustments

                    # Click using JavaScript to bypass interception
                    driver.execute_script("arguments[0].click();", pdf_element)
                    time.sleep(1)  # Optional delay to prevent rapid clicking issues

                except Exception as e:
                    print(f"Error clicking element: {e}")

            # Wait until the "next page" button is clickable before clicking
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "flipRight"))).click()
            time.sleep(2)

            # Re-fetch the "next page" element
            next_page = driver.find_element(By.CLASS_NAME, "flipRight")
        
        year = driver.find_element(By.ID, f"{i}.[anno]")
        year.click()
            
    # except:
    #     print("-------------------")
    #     pass
    driver.close()    
    
ScrapeList()



# def ScrapeList(start = 2010, end = 2010):
#     baseUrl = "https://www.normattiva.it/ricerca/elencoPerData"
#     data = []
#     download_dir = f'{os.getcwd()}\\download'
#     driver = Driver(uc=True)
#     pdf_files = [file for file in os.listdir(download_dir) if file.endswith('.pdf')]
#     for year in range(start, end + 1, 1):
#         print("Current Year :    ", year)
#         try:
#             driver.get(f'{baseUrl}/anno/{year}')
#             current_page = 0
#             driver.get(f'{baseUrl}/{current_page}')
#             card = driver.find_elements(By.XPATH, "//div[starts-with(@id, 'heading_')]")
#             while len(card):
#                 try:
#                     for i in range(len(card)):
#                         try:           
#                             href = card[i].find_element(By.CSS_SELECTOR, 'p > a').get_attribute("href")    
#                             parsed_url = urlparse(href)
#                             query_params = parse_qs(parsed_url.query)
#                             date = query_params.get('atto.dataPubblicazioneGazzetta', [None])[0]
#                             code = query_params.get('atto.codiceRedazionale', [None])[0]
#                             # check if current file has been downloaded
#                             download_dir = f'{os.getcwd()}\\download'
#                             match = any(file.startswith(f'{date}_{code}') for file in pdf_files)
#                             if match:
#                                 print(date)
#                                 continue
                            
#                             card[i].find_element(By.CSS_SELECTOR, 'p > a').click()
#                             driver.get(f'https://www.normattiva.it/atto/vediMenuExport?atto.dataPubblicazioneGazzetta={date}&atto.codiceRedazionale={code}&currentSearch=')
#                             pdf_button = driver.find_element(By.NAME, 'downloadPdf')
#                             pdf_button.click()
#                             time.sleep(3)
#                             driver.switch_to.window(driver.window_handles[1])
#                             element = driver.find_element(By.TAG_NAME, 'body')
#                             action = ActionChains(driver)
#                             action.move_to_element(element).click().perform()
                            
#                             pyautogui.hotkey('ctrl', 's')
#                             time.sleep(1)
#                             pyautogui.write(f'{download_dir}\\{date}_{code}.pdf')
#                             time.sleep(1)
#                             pyautogui.hotkey('enter')
#                             time.sleep(1)

#                             driver.close()
#                             driver.switch_to.window(driver.window_handles[0])
#                             driver.back()
#                             driver.back()
#                             card = driver.find_elements(By.XPATH, "//div[starts-with(@id, 'heading_')]")
#                         except:
#                             pass
#                     current_page += 1
#                     driver.get(f'{baseUrl}/{current_page}')
#                     card = driver.find_elements(By.XPATH, "//div[starts-with(@id, 'heading_')]")
#                 except:
#                     pass
#         except:
#             pass

#     driver.close()    

