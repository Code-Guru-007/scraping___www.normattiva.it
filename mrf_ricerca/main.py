import os
import datetime

import daily_scrape
import upload


if __name__ == "__main__":
    base_dir = "download"
    year = datetime.datetime.now().year
    directory_path = os.path.join(base_dir, str(year))
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created.")
    else:
        print(f"Directory '{directory_path}' already exists.")
    # for year in range(1970, 2026):
    daily_scrape.ScrapeList(2010)
    # upload.UploadPdf(year)
        