import os
import urllib.parse
import requests
import ssl
import time
from fake_useragent import UserAgent

def load_proxies(file_path="proxy.txt"):
    """Load proxies from file."""
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]

def download_pdf(year, url_source):
    """Download PDFs while handling CAPTCHAs and logging failed URLs."""
    context = ssl._create_unverified_context()
    download_dir = os.path.join(os.getcwd(), 'download', 'normattiva_local', year)
    os.makedirs(download_dir, exist_ok=True)

    # Load URLs
    with open(os.path.join(download_dir, url_source), "r") as file:
        pdf_urls = [f'{line.strip()}' for line in file.readlines()]
    
    proxies_list = load_proxies()
    total_count = len(pdf_urls)
    session = requests.Session()
    ua = UserAgent()

    for i, escaped_url in enumerate(pdf_urls):
        proxy = {"http": f"http://{proxies_list[i % len(proxies_list)]}", "https": f"http://{proxies_list[i % len(proxies_list)]}"}  # Rotate proxies
        url = urllib.parse.unquote(f'https://www.italgiure.giustizia.it{escaped_url}')
        headers = {"User-Agent": ua.random, "Accept-Language": "en-US,en;q=0.9"}

        try:
            filename = url.split("./")[1].replace("/", "_")
            pdf_dir = os.path.join(download_dir, filename.split("_")[0])
            os.makedirs(pdf_dir, exist_ok=True)
            
            file_path = os.path.join(pdf_dir, filename)
            if os.path.exists(file_path):
                print(f"[{i+1}/{total_count} Skipping existing file: {filename}")
                continue
            
            response = session.get(url, headers=headers, proxies=proxy, timeout=10, verify=False)
            time.sleep(3)  # Prevent rapid requests
            content = response.content

            if b'captcha' in content.lower():
                print(f"[{i+1}/{total_count}] CAPTCHA detected. Logging failed URL: {url}")
                with open("failed.txt", "a") as f:
                    f.write(url + "\n")
                time.sleep(60)
                continue
            
            with open(os.path.join(pdf_dir, filename), "wb") as file:
                file.write(content)
            
            with open(os.path.join(download_dir, "pdf_url.txt")) as file:
                file.write(escaped_url + '\n')
            print(f"[{i+1}/{total_count}] Downloaded: {filename}")
        
        except Exception as e:
            print(f"[{i+1}/{total_count}] Failed to download {url}: {e}")
            with open("failed.txt", "a") as f:
                f.write(url + "\n")
    
    download_pdf(year, "failed.txt")
        

if __name__ == "__main__":
    download_pdf()
