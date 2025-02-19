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

# Set Chrome options
options = Options()
# options.add_argument("--headless=new")  # Uncomment if you want headless mode

# Start the WebDriver
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    seleniumwire_options=seleniumwire_options,
    options=options
)

for year in range(2015, 2025):
    try:
        # Open the webpage
        driver.get("https://def.finanze.it/DocTribFrontend/RS2_HomePage.jsp")
        download_dir = os.path.join(os.getcwd(), "download", str(year))
        os.makedirs(download_dir, exist_ok=True)

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
                        with open(os.path.join(download_dir, f"{id}.txt"), 'a') as f:
                            if result[0] == '{':
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
