import os
import re
import requests



with open(os.path.join(os.getcwd(), 'session.txt'), 'r') as file:
    id_session = file.readline().strip()
    
cookies = {
    'cookie_consent_user_accepted': 'true',
    'cookie_consent_level': '%7B%22strictly-necessary%22%3Atrue%2C%22functionality%22%3Atrue%7D',
    # 'idsessione': "ba7a2b47e8cdad0f81548911e6e139e3",
    'idsessione': id_session,
    # 'idsessione': "5ac2958fcc3c7937fea98b1165da3b76",
    # 'profile': "3",
    # 'uname': 'unknown'
    
}

# proxy = {
#     "http": "http://dBmTABWe6lHt7Lzi:7hsc7iCVnOMLTmGO@geo.iproyal.com:12321",
#     "https": "http://dBmTABWe6lHt7Lzi:7hsc7iCVnOMLTmGO@geo.iproyal.com:12321"
# }
proxy = {
    "http": "http://c7fjetgtletu:JXTWkrkRsUQFsVcb@104.234.48.92:6010",
    "https": "http://c7fjetgtletu:JXTWkrkRsUQFsVcb@104.234.48.92:6010"
}

# url = "https://www.ilmerito.it/download_sentenza.php?mid=61202&id=52323"
# res = requests.get(url, cookies=cookies, proxies=proxy)

# error = "Errore! Contenuto non disponibile."

# match = re.search(r'filename="(.+?)"', res.headers.get("Content-Disposition", ""))
# filename = match.group(1) if match else None


# if res.status_code == 200:
#     with open("test.pdf", 'wb') as file:
#         file.write(res.content)
for year in range(2016, 2025):
    current = 0
    download_dir = os.path.join(os.getcwd(), "download", str(year))
    urls = []
    os.makedirs(download_dir, exist_ok=True)
    if os.path.exists(f"{year}_pdf.txt"):
        with open(f"{year}_pdf.txt", "r") as file:
            urls = [line.strip() for line in file.readlines()]
    total = len(urls)
    if year == 2014:
        s_num = 381
    else:
        s_num = 0
            
    for url in urls:
        try:
            current += 1
            downloaded_url = []
            if(os.path.exists("downloaded_pdf.txt")):
                with open("downloaded_pdf.txt", "r") as file:
                    downloaded_url = [line.strip() for line in file.readlines()]
            if url in downloaded_url:
                print(f"[{year}=>   {current}  /  {total}]  Already Downloaded!")
                continue
            res = requests.get(url, cookies=cookies, proxies=proxy)
            if res.status_code == 200:
                match = re.search(r'filename="(.+?)"', res.headers.get("Content-Disposition", ""))
                filename = match.group(1) if match else None
                error = "Errore! Contenuto non disponibile."
                if res.text == error:
                    print(f"[{year}=>   {current}  /  {total}]    Failed")
                    with open(os.path.join(download_dir, "failed.txt"), 'a') as file:
                        file.write(f"{url}\n")
                    continue
                
                if not filename:
                    print(f"[{year}=>   {current}  /  {total}]    Filename missing, skipping download")
                    with open(os.path.join(download_dir, "failed.txt"), 'a') as file:
                        file.write(f"{url}\n")
                    continue  # Skip this file and move to the next URL

                filename = re.sub(r'[\/:*?"<>|]', '_', filename)
                
                if filename == "sentenza.pdf":
                    s_num += 1
                    with open(os.path.join(download_dir, f"{filename.split(".")[0]}_{s_num}.pdf"), 'wb') as file:
                        file.write(res.content)
                    print(f"[{year}=>   {current}  /  {total}]  Downloaded: {filename.split(".")[0]}_{s_num}.pdf")
                else:
                    with open(os.path.join(download_dir, filename), 'wb') as file:
                        file.write(res.content)

                    print(f"[{year}=>   {current}  /  {total}]  Downloaded: {filename}")

                with open("downloaded_pdf.txt", "a") as file:
                    file.write(f"{url}\n")
            else:
                print("Error occur!")
                
        except Exception as e:
            print(e)