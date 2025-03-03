import requests
from seleniumbase import Driver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from urllib.parse import urlparse, parse_qs
import time
import os

cookies = {
    'cookie_consent_user_accepted': 'true',
    'cookie_consent_level': '%7B%22strictly-necessary%22%3Atrue%2C%22functionality%22%3Atrue%7D',
    'idsessione': "d76a1a25c8482568c15d2af5108550a0",
    # 'idsessione': "5ac2958fcc3c7937fea98b1165da3b76",
    # 'profile': "3",
    # 'uname': 'unknown'
    
}

driver = driver = Driver(uc=True)
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

for year in range(2011, 2025):
    total = []
    for month in range(1, 13):
        url = F"https://www.ilmerito.it/bancadati/index.php?pag_id=43&mm={month}&aa={year}&tipo=4"
        
        driver.get(url)

        options_in_select = driver.find_elements(By.XPATH, '//select[@name="npag"]/option')
        option_count = len(options_in_select)
        
        
        for i in range(1, option_count + 1):
            print(f"[{i} / {option_count}]")
            options_in_select = driver.find_elements(By.XPATH, '//select[@name="npag"]/option')
            links = driver.find_elements(By.XPATH,'//a[@title="visualizza massima"]')
            for link in links:
                total.append(link.get_attribute("href"))
                with open(f'{str(year)}.txt', 'a') as file:
                    file.write(f"{link.get_attribute("href")}\n")  
                print(link.get_attribute("href"))
            #     file.write(res.content)
            if i != option_count:
                options_in_select[i].click()
                time.sleep(3)
      