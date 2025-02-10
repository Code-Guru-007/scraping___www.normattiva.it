import urllib.parse
import requests

url = urllib.parse.unquote("https://www.italgiure.giustizia.it/xway/application/nif/clean/hc.dll%3Fverbo%3Dattach%26db%3Dsnpen%26id%3D./20250206/snpen@s70@a2025@n04986@tO.clean.pdf")
response = requests.get(url, stream=True)
print(url)
if response.status_code == 200:
    with open(f'test.pdf', "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
    print(f"Download complete: test.pdf")
else:
    print("Failed to download. Status Code:", response.status_code)