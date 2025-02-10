import os
import time
import requests
import urllib.parse
from fake_useragent import UserAgent

# Load proxies from proxy.txt
def load_proxies(file_path="proxy.txt"):
    with open(file_path, "r") as file:
        proxies = [{"http": line.strip(), "https": line.strip()} for line in file.readlines()]
    return proxies

# Download PDFs using rotating proxies
def download_pdf(year):
    download_dir = os.path.join(os.getcwd(), "download", str(year))
    os.makedirs(download_dir, exist_ok=True)

    # Load URLs from file
    with open(f"{year}.txt", "r") as file:
        pdf_urls = [f'https://www.italgiure.giustizia.it{line.strip()}' for line in file.readlines()]

    proxies_list = load_proxies()  # Load proxies
    total_count = len(pdf_urls)

    for i, escaped_url in enumerate(pdf_urls):
        proxy = proxies_list[i % len(proxies_list)]  # Rotate proxies
        headers = {"User-Agent": UserAgent().random}
        url = urllib.parse.unquote(escaped_url)

        try:
            response = requests.get(url, headers=headers, stream=True, proxies=proxy, verify=False, timeout=10)

            if response.status_code == 200:
                filename = url.split("./")[1].replace("/", "_")
                pdf_dir = os.path.join(download_dir, filename.split("_")[0])
                os.makedirs(pdf_dir, exist_ok=True)

                with open(os.path.join(pdf_dir, filename), "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)

                print(f"[{i+1}/{total_count}] Downloaded: {filename}")
            else:
                print(f"[{i+1}/{total_count}] Failed to download ({response.status_code}): {url}")

        except requests.exceptions.RequestException as e:
            print(f"[{i+1}/{total_count}] Error: {e}")

        time.sleep(3)  # Avoid being blocked


    
    # if os.path.exists(f"{download_dir}\\download_url.txt"):
    #     os.remove(f"{download_dir}\\download_url.txt")
    #     print("File deleted successfully.")
    # else:
    #     print("File not found.")


download_pdf(2025)