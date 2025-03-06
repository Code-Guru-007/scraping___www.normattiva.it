from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os

def ScrapeList(year):
    baseUrl = "https://apps.dirittopratico.it/sentenze.html"
    download_dir = os.path.join(os.getcwd(), "download", str(year))
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
    driver.get(baseUrl)

    try:
        cookie_ok = driver.find_element(By.ID, "cookieChoiceDismiss")
        cookie_ok.click()
    except:
        pass

    # Enter Year
    year_input = driver.find_element(By.XPATH, "//input[@name='data']")
    year_input.clear()
    year_input.send_keys(year)

    # Select an Option
    options_in_select = driver.find_elements(By.XPATH, '//select[@name="nris"]/option')
    options_in_select[3].click()

    # Click Search
    search_btn = driver.find_element(By.XPATH, "//input[@name='search']")
    search_btn.click()

    total = int(driver.find_element(By.ID, "contres").text.split(" ")[0])
    
    downloaded_title = []
    if os.path.exists(os.path.join(download_dir, "downloaded.txt")):
        with open(os.path.join(download_dir, "downloaded.txt"), 'r') as file:
            downloaded_title = [line.strip() for line in file.readlines()]
    
    i = 0
    current = 0
    while i < total / 20 + 1:
    # while i < 180:
        try:

            # Extract all provvedimento elements
            html_contents = driver.find_elements(By.CLASS_NAME, "provvedimento")

            print(len(html_contents))
            
            for item in html_contents:
                print(f"[ {current}  /  {total}]")
                current += 1
                t_title = item.find_element(By.TAG_NAME, "h3").text
                b_title = item.find_element(By.CSS_SELECTOR, "p.infoB").text.split(":")[0]
                title = f"{t_title} {b_title}"
                if title in downloaded_title:
                    continue
                pdf_download = item.find_element(By.TAG_NAME, 'a')
                pdf_download.click()
                print(title)
                time.sleep(2)
                pdf_files = [f for f in os.listdir(download_dir) if f.endswith(".pdf")]
                # Get the most recently modified PDF file
                if pdf_files:
                    latest_pdf = max(
                        (os.path.join(download_dir, f) for f in pdf_files), 
                        key=os.path.getmtime
                    )
                    filename = os.path.basename(latest_pdf)
                else:
                    print("     No PDF files found in the directory.")
                print(filename)
                old_path = os.path.join(download_dir, filename)
                new_path = os.path.join(download_dir, f"{title}.pdf")
                rename_file(old_path, new_path)
                
                with open(os.path.join(download_dir, "downloaded.txt"), 'a') as file:
                    file.write(f"{title}\n")
                time.sleep(1)

            # Click Next Page
            next_page = driver.find_element(By.XPATH, "//button[@name='avanti']")
            next_page.click()
            i += 1

        except Exception as e:
            print(e)

    time.sleep(10)
    driver.quit()    

def rename_file(old_path, new_path):
    if os.path.exists(old_path):
        os.rename(old_path, new_path)

ScrapeList(2020)
