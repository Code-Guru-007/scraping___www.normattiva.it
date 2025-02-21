import os
import datetime

import daily_scrape
# import upload


if __name__ == "__main__":

    base_dir = "download/normative"
    year = datetime.datetime.now().year
    directory_path = os.path.join(base_dir, str(year))
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"{datetime.datetime.now()}:      Directory '{directory_path}' created.")
    else:
        print(f"{datetime.datetime.now()}:      Directory '{directory_path}' already exists.")
    daily_scrape.ScrapeList(year)
    # upload.UploadPdf(year)
        