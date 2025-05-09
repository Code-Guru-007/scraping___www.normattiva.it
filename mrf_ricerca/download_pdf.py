import os
import re
import requests
import pdfkit
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


proxy = {
    "http": "http://dBmTABWe6lHt7Lzi:7hsc7iCVnOMLTmGO@geo.iproyal.com:12321",
    "https": "http://dBmTABWe6lHt7Lzi:7hsc7iCVnOMLTmGO@geo.iproyal.com:12321"
}

download_dir = "downloaded_pdf"

def extract_filename_from_headers(response):
    """Extract filename from content-disposition header"""
    content_disp = response.headers.get('content-disposition', '')
    if not content_disp:
        return None
    
    # Match filename in content-disposition header
    match = re.search(r'filename="?(.+?)"?(;|$)', content_disp)
    if match:
        return match.group(1)
    return None

def print_pdf(main_tag, year, title):
    html_template = f'''
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body>
        {str(main_tag)}
    </body>
    </html>
    '''

    pdfkit.from_string(html_template, f"downloaded_pdf/{year}/{title}.pdf")
    print("PDF saved as 'main_content.pdf'")

def download_pdf_from_url(url):
    response = requests.get(url, stream=True, proxies=proxy, verify=False)
    response.raise_for_status()  # Raise an error for bad status codes
    filename = extract_filename_from_headers(response)
    file_path = os.path.join(download_dir, f"{year}/{filename}")

    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

    print(f"PDF successfully saved to: {file_path}")


for year in range(1970, 2026):
    os.makedirs(f"downloaded_pdf/{year}", exist_ok=True)
    with open(f"list/{year}.txt") as file:
        url_lists = [line.strip() for line in file.readlines()]
    for url in url_lists:
        # if url.startswith("http://www.consiglio.vda.it"):
        #     try:
        #         print(url)
        #         response = requests.get(url, proxies=proxy)
        #         response.raise_for_status()  # Raise an exception for HTTP errors
        #         soup = BeautifulSoup(response.text, 'html.parser')
        #         main_tag = soup.find('main', {'id': 'contenuto-principale'})
        #         title = main_tag.find('h1').get_text(strip=True)
                
        #         if main_tag:
        #             print_pdf(main_tag, year, title)

        #     except requests.exceptions.RequestException as e:
        #         print("Error fetching the URL:", e)
        # if url.startswith("https://lexview-int.regione.fvg.it/"):
        #     try:
        #         print(url)
        #         response = requests.get(url, proxies=proxy)
        #         response.raise_for_status()  # Raise an exception for HTTP errors
        #         soup = BeautifulSoup(response.text, 'html.parser')
        #         a_tag = soup.find('a', {'id': 'PageBody_hlLeggeIntera'})
        #         pdf_url = f"https://lexview-int.regione.fvg.it/FontiNormative/xml/{soup.find('a', {'id': 'PageBody_aPdf'})['href']}"
        #         title = a_tag.get_text(strip=True)
        #         print(title)
        #         try:
        #             # Send GET request
        #             response = requests.get(pdf_url, stream=True, proxies=proxy)
        #             response.raise_for_status()  # Raise an error for bad status codes

        #             # Full path for the PDF file
        #             file_path = os.path.join(download_dir, f"{year}/{title}.pdf")

        #             # Save the PDF
        #             with open(file_path, 'wb') as f:
        #                 for chunk in response.iter_content(chunk_size=8192):
        #                     if chunk:  # filter out keep-alive new chunks
        #                         f.write(chunk)

        #             print(f"PDF successfully saved to: {file_path}")
        #         except Exception as e:
        #             print(f"Error downloading the PDF: {e}")

        #     except Exception as e:
        #         print(e)

        # if url.startswith("http://www.consrc.it"):
        #     download_pdf_from_url(url)
        # elif url.startswith("http://raccoltanormativa.consiglio.regione.toscana.it"):
        #     print(url)
        #     response = requests.get(url, proxies=proxy, verify=False)
        #     response.raise_for_status()  # Raise an exception for HTTP errors
        #     soup = BeautifulSoup(response.text, 'html.parser')
        #     pdf_url = soup.find('a', {'title': 'Scarica il documento corrente in formato PDF'})['href']
        #     download_pdf_from_url(f"http://raccoltanormativa.consiglio.regione.toscana.it/{pdf_url}")
        # if url.startswith("https://www.consiglio.regione.lazio.it"):
        #     response = requests.get(url, proxies=proxy)
        #     response.raise_for_status()  # Raise an exception for HTTP errors
        #     soup = BeautifulSoup(response.text, 'html.parser')
        #     main_tag = soup.find('div', {'id': 'contenuto_legge'})
        #     page_title_div = soup.find('div', id='page-title')
        #     title = page_title_div.find_all('a')[-1].get('title', 'No title attribute')
            
        #     if main_tag:
        #         print_pdf(main_tag, year, title)
        # if url.startswith("https://demetra.regione.emilia-romagna.it"):
        #     print(url)
        #     response = requests.get(url, proxies=proxy, verify=False)
        #     response.raise_for_status()  # Raise an exception for HTTP errors
        #     soup = BeautifulSoup(response.text, 'html.parser')
        #     pdf_url = soup.find('a', {'title': 'Scarica il documento corrente in formato PDF3'})['href']
        #     download_pdf_from_url(f"https://demetra.regione.emilia-romagna.it/al/{pdf_url}")
        # if url.startswith("https://www.consiglio.marche.it"):
        #     response = requests.get(url, proxies=proxy, verify=False)
        #     response.raise_for_status()  # Raise an exception for HTTP errors
        #     soup = BeautifulSoup(response.text, 'html.parser')
        #     title_tag = soup.find('section', {'id': 'intro'})
        #     content_tag = soup.find('div', {'id': 'atto'})
        #     title = content_tag.find_all('td')[1].get_text('strip=True')
        #     main_tag = f"{title_tag} {content_tag}"
        #     print_pdf(main_tag, year, title)
        # if url.startswith("https://normelombardia.consiglio.regione.lombardia.it"):
        #     print(url)
        #     parsed_url = urlparse(url)
        #     query_params = parse_qs(parsed_url.query)
        #     iddoc = query_params.get('iddoc', [None])[0]
        #     download_pdf_from_url(f"https://normelombardia.consiglio.regione.lombardia.it/accessibile/esportaDoc.aspx?type=pdf&iddoc={iddoc}")
        # if url.startswith("http://bussolanormativa.consiglio.puglia.it"):
        #     print(url)
        #     response = requests.get(url, proxies=proxy, verify=False)
        #     response.raise_for_status()  # Raise an exception for HTTP errors
        #     soup = BeautifulSoup(response.text, 'lxml')
        #     main_tag = soup.find('tbody')
        #     title = main_tag.find('span', {'id': 'ContentPlaceHolder1_lblTesto'}).find('div', {'class':'corpo'}).find_all('p')[0].get_text('strip=True')
        #     print_pdf(main_tag, year, title)
        # if url.startswith("http://atticonsiglio.consiglio.basilicata.it"):
        #     print(url)
        #     response = requests.get(url, proxies=proxy, verify=False)
        #     response.raise_for_status()  # Raise an exception for HTTP errors
        #     soup = BeautifulSoup(response.text, 'lxml')
        #     main_tag = soup.find('div', {'class': 'WordSection1'})
        #     title = main_tag.find('p', {'class':'Legge'}).get_text('strip=True')
        #     print_pdf(main_tag, year, title)



