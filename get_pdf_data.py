import os
import re
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def ScrapeList(year, waiting_time):
    baseUrl = "https://apps.dirittopratico.it/sentenze.html"
    download_dir = os.path.join(os.getcwd(), "download", str(year))
    os.makedirs(download_dir, exist_ok=True)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
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
    time.sleep(10)
    element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "contres"))
        )
    total = int(element.text.strip().split(" ")[0])
    
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

            
            for item in html_contents:
                current += 1
                print(f"[ {current}  /  {total}]")
                t_title = item.find_element(By.TAG_NAME, "h3").text.replace("/", "-")
                b_title = item.find_element(By.CSS_SELECTOR, "p.infoB").text
                code = extract_code(b_title)
                if not code:
                    preview_text = item.find_element(By.CSS_SELECTOR, "div.estratto > p").text
                    code = extract_code(preview_text)
                title = f"{t_title} {code}"
                if title in downloaded_title:
                    continue
                pdf_download = item.find_element(By.TAG_NAME, 'a')
                pdf_download.click()
                time.sleep(int(waiting_time))
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
                old_path = os.path.join(download_dir, filename)
                new_path = os.path.join(download_dir, f"{title}.pdf")
                rename_file(old_path, new_path)
                
                if total > 9997:
                    try:
                        new_dir = filename.split(",")[0]
                        print(new_dir)
                        os.makedirs(os.path.join(download_dir, new_dir), exist_ok=True)
                        shutil.move(new_path, os.path.join(download_dir, new_dir))
                    except Exception as e:
                        print(e)
                
                with open(os.path.join(download_dir, "downloaded.txt"), 'a') as file:
                    file.write(f"{title}\n")

            # Click Next Page
            next_page = driver.find_element(By.XPATH, "//button[@name='avanti']")
            next_page.click()
            i += 1
        except TimeoutError as e:
            driver.refresh()


    time.sleep(10)
    driver.quit()    

def sanitize_filename(filename):
    """Replace invalid characters in the filename for Windows."""
    return re.sub(r'[\/:*?"<>|]', '_', filename)  # Replace invalid characters with "_"

def rename_file(old_path, new_path, max_retries=10):
    """Attempt to rename the file safely, ensuring it exists and handling errors."""
    # sanitized_new_path = os.path.join(os.path.dirname(new_path), sanitize_filename(os.path.basename(new_path)))

    # Ensure the file exists before renaming
    if not os.path.exists(old_path):
        print(f"Error: File does not exist - {old_path}")
        return

    # Retry logic for renaming (useful if file is still being downloaded)
    for attempt in range(max_retries):
        try:
            os.rename(old_path, new_path)
            print(f"Renamed successfully: {new_path}")
            return
        except FileNotFoundError:
            print(f"Retry {attempt + 1}/{max_retries}: File not found, waiting...")
            time.sleep(2)  # Wait for file to appear
        except PermissionError:
            print(f"Retry {attempt + 1}/{max_retries}: File in use, waiting...")
            time.sleep(2)  # Wait in case file is still downloading
        except Exception as e:
            print(f"Unexpected error renaming file: {e}")
            return

    print(f"Failed to rename file after {max_retries} retries.")

def extract_code(text):
    # Regular expression to match {number}/{year} or {number}-{year}
    pattern = r'(\d+)[-/](\d{4})'
    
    # Search for the pattern in the text
    match = re.search(pattern, text)
    
    if match:
        number, year = match.groups()
        # Replace / with - to standardize
        return f"{number}-{year}"
    return None

year = input("input year:  ")
waiting_time = input("download time:  ")
ScrapeList(year, waiting_time)
