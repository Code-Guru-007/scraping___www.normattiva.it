from seleniumbase import Driver
from selenium.webdriver.common.by import By
import time
import os

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

for year in range(2019, 2025):
    with open(f'{year}.txt', 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    total = len(urls)
    current = 0
    for url in urls:
        try:
            current += 1
            downloaded_url = []
            if(os.path.exists("downloaded.txt")):
                with open("downloaded.txt", "r") as file:
                    downloaded_url = [line.strip() for line in file.readlines()]
            if url in downloaded_url:
                print(f"[{year}=>   {current}  /  {total}]  Already Downloaded!")
                continue
            driver.get(url)
            a_tag = driver.find_element(By.XPATH, "//font[@class='black12']/a")
            with open(f"{year}_pdf.txt", 'a') as file:
                file.write(f"{a_tag.get_attribute("href")}\n")
            print(f"[{year}=>   {current}  /  {total}]")
            with open(f"downloaded.txt", "a") as file:
                file.write(f"{url}\n")
        except Exception as e:
            with open(f"fail_pdf_link.txt", "a") as file:
                file.write(f"{url}\n")
            