import os
import datetime

import scrape_list
import download_pdf


if __name__ == "__main__":
    year = datetime.datetime.now().year
    download_dir = os.path.join(os.getcwd(), "download", "def.finanze.it", str(year))
    os.makedirs(download_dir, exist_ok=True)
    os.chmod(download_dir, 0o777)
    scrape_list.get_scrape_list(year)
    download_pdf.download_pdf(download_dir, year)
    