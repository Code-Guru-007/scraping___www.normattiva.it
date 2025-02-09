import requests
import urllib.parse
import os

# Unescape the URL

def download_pdf(year):
    download_dir = f'{os.getcwd()}\\download\\www.italgiure.giustizia.it\\{year}'
    with open("pdf_url.txt", "r") as file:
        pdf_urls = [f'https://www.italgiure.giustizia.it{line.strip()}' for line in file.readlines()]  # Remove whitespace/newlines

        
    # escaped_url = "https://www.italgiure.giustizia.it/xway/application/nif/clean/hc.dll%3Fverbo%3Dattach%26db%3Dsnpen%26id%3D./20250206/snpen@s70@a2025@n04987@tO.clean.pdf"

    # Send GET request
    for escaped_url in pdf_urls:
        url = urllib.parse.unquote(escaped_url)  # Unescape the URL
        filename = url.split("./")[1].replace("/", "_")
        response = requests.get(url, stream=True)
        
        pdf_files = [file for file in os.listdir(download_dir) if file.endswith('.pdf')]

        match = any(file.startswith(filename) for file in pdf_files)
        if match:
            print("Already Downloaded :  ", filename)
            continue

        # Check if the request was successful
        if response.status_code == 200:
            with open(f'{download_dir}\\{filename}', "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
                with open(f'{download_dir}\\downloaded_file.txt', "a") as f:
                    f.write(f"{filename}\n")
            print(f"Download complete: {filename}")
        else:
            print("Failed to download. Status Code:", response.status_code)