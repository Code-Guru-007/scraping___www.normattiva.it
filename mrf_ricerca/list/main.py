import re
from urllib.parse import urlparse
import os

def extract_urls(file_path):
    urls = set()
    url_pattern = re.compile(r'(https?://[^\s/$.?#].[^\s]*)')
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        found_urls = url_pattern.findall(content)
        for url in found_urls:
            try:
                # Validate and normalize the URL while preserving protocol and subdomains
                parsed = urlparse(url)
                if parsed.scheme and parsed.netloc:
                    # Keep the full URL with protocol and subdomains
                    normalized_url = f"{parsed.scheme}://{parsed.netloc}".lower()
                    urls.add(normalized_url)
            except:
                continue
    return urls

def process_files():
    all_urls = set()
    
    for year in range(1970, 2026):
        filename = f"{year}.txt"
        if os.path.exists(filename):
            urls = extract_urls(filename)
            all_urls.update(urls)
    
    # Save unique URLs to a file
    with open('unique_urls_with_protocol.txt', 'w') as outfile:
        for url in sorted(all_urls):
            outfile.write(url + '\n')
    
    print(f"Found {len(all_urls)} unique URLs (with protocol and subdomains)")

if __name__ == "__main__":
    process_files()