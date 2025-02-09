import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Year Mapping
anno = {
    '2025': 1,
    '2024': 2,
    '2023': 3,
    '2022': 4,
    '2021': 5,
    '2020': 6,
}




def get_scrape_list(year):
    """Scrapes PDF links for a given year and saves them to a text file."""
    base_url = "https://www.italgiure.giustizia.it/sncass/"
    count = 0
    pdf_urls = [""]
    download_dir = f'{os.getcwd()}\\download\\www.italgiure.giustizia.it\\{year}'
    
    if os.path.exists(f"{download_dir}\\pdf_url.txt"):
        with open(f"{download_dir}\\pdf_url.txt", "r") as file:
            pdf_urls = [line.strip() for line in file.readlines()]
        
    chrome_options = Options()

    driver = webdriver.Chrome(options=chrome_options)
    chrome_options.add_argument("--headless")
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(base_url)
        time.sleep(2)

        # Select the year
        year_element = driver.find_element(By.ID, f"{anno.get(str(year))}.[anno]")
        year_element.click()
        time.sleep(2)

        # Get the next page button
        next_page = driver.find_element(By.CLASS_NAME, "flipRight")

        while next_page.value_of_css_property("display") != "none":
            # Wait for PDF elements
            pdf_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "text2pdf")))

            for pdf_element in pdf_elements:
                try:
                    # Scroll into view
                    # driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pdf_element)
                    # time.sleep(0.5)

                    # Extract PDF URL
                    url = pdf_element.find_element(By.CSS_SELECTOR, ".toDocument.pdf").get_attribute("data-arg")
                    if url in pdf_urls:
                        print(f"Already added: {url}")
                        continue
                    count += 1
                    print(f"{count} >> {url}")

                    # Save to file
                    with open(f"{download_dir}\\pdf_url.txt", 'a') as f:
                        f.write(url + "\n")

                except Exception as e:
                    print(f"Error processing element: {e}")

            # Move to the next page
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "flipRight"))).click()
            time.sleep(2)

            # Re-fetch the "next page" element
            next_page = driver.find_element(By.CLASS_NAME, "flipRight")

    except Exception as e:
        print(f"Error in scrape_list: {e}")

    finally:
        driver.quit()


# Run the script for the year 2025
# year = 2025
# scrape_list(year)
