from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os

import time

# Configure the proxy
proxy_username = "dBmTABWe6lHt7Lzi"
proxy_password = "7hsc7iCVnOMLTmGO"
proxy_address = "geo.iproyal.com"
proxy_port = "12321"

proxy_url = f"http://{proxy_username}:{proxy_password}@{proxy_address}:{proxy_port}"

seleniumwire_options = {
    "proxy": {
        "http": proxy_url,
        "https": proxy_url
    },
}


def get_scrape_list(year):
    try:
        downloaded_list = []
        download_dir = os.path.join(os.getcwd(), 'download', 'def.finanze.it', str(year))
        os.makedirs(download_dir, exist_ok=True)
        #################################
        ##### Selenium Setting   #####
        #################################
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--remote-debugging-port=9222")  # Debugging port
        # chrome_options.add_argument("--user-data-dir=/tmp/chrome_profile")
        chrome_options.add_experimental_option('prefs',  {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
            }
        )
        # options.add_argument("--headless=new")  # Uncomment if you want headless mode

        # Start the WebDriver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            seleniumwire_options=seleniumwire_options,
            options=chrome_options
        )
        ###################################
        ###################################
        # Open the webpage
        driver.get("https://def.finanze.it/DocTribFrontend/RS2_HomePage.jsp")

        input_field = driver.find_element(By.ID, "anno")
        input_field.clear()  # Clear existing value
        input_field.send_keys(str(year))

        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        ids = ["normativaLink", "prassiLink", "giurisprudenzaLink"]
        # ids = ["prassiLink", "giurisprudenzaLink"]
        for id in ids:
            filter = driver.find_element(By.ID, id)
            filter.click()

            page_selectors = ["a.avanti", "a.ulteriori"]
            current_page = 1
            last_page = False
            while True:
                for i in range(5):
                    link_container = driver.find_element(By.CSS_SELECTOR, "div.risultati-ricerca")
                    links = link_container.find_elements(By.TAG_NAME, "a")
                    for link in links:
                        result = link.get_attribute('href').split('=')[-1]
                        if os.path.exists(os.path.join(download_dir, f'{id}.txt')):
                            with open(os.path.join(download_dir, f'{id}.txt'), 'r') as file:
                                downloaded_id = [line.strip() for line in file.readlines()]
                        if result not in downloaded_id and result.startswith('{'):
                            with open(os.path.join(download_dir, f"{id}.txt"), 'a') as f:
                                # if result[0] == '{':
                                f.write(f'{result}\n')
                    current_page += 1
                    next_page = driver.find_elements(By.CSS_SELECTOR, "a.avanti")[0]
                    pagination = driver.find_elements(By.CSS_SELECTOR, "a.ulteriori")[0]
                    
                    if next_page.value_of_css_property("display") == "none" and pagination.value_of_css_property("display") == "none":
                        print("Last page")
                        last_page = True
                        break
                    if i != 4: 
                        next_page.click()
                if last_page:
                    break
                driver.get("https://def.finanze.it/DocTribFrontend/paginatorXml.do")
                # time.sleep(1)
            # time.sleep(2)

    except:
        pass
    # finally:
    #     # Quit the driver
    #     driver.quit()
    driver.quit()
