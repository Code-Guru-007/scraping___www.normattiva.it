from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os



def get_scrape_list(year):
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
    pdf_urls = []
    if os.path.exists(os.path.join(download_dir, "pdf_urls.txt")):
        with open(os.path.join(download_dir, "pdf_urls.txt"), "r") as file:
            pdf_urls = [line.strip() for line in file.readlines()]
    for month in range(1, 13):
        url = F"https://www.ilmerito.it/bancadati/index.php?pag_id=43&mm={month}&aa={year}&tipo=4"
        
        driver.get(url)

        try:
            options_in_select = driver.find_elements(By.XPATH, '//select[@name="npag"]/option')
            option_count = len(options_in_select)
        except:
            break
        
        for i in range(1, option_count + 1):
            print(f"[{i} / {option_count}]")
            options_in_select = driver.find_elements(By.XPATH, '//select[@name="npag"]/option')
            links = driver.find_elements(By.XPATH,'//a[@title="visualizza massima"]')
            for link in links:
                pdf_url = link.get_attribute("href")
                if pdf_url in pdf_urls:
                    print("Already Exists!")
                    continue
                with open(os.path.join(download_dir, 'buf.txt'), 'a') as file:
                    file.write(f"{pdf_url}\n")  
                print(pdf_url)
            #     file.write(res.content)
            if i != option_count:
                options_in_select[i].click()
                time.sleep(3)
    driver.quit()