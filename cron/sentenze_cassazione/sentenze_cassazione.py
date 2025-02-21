import os
import datetime

import local_scrape


if __name__ == "__main__":
    base_dir = "download"
    year = datetime.datetime.now().year
    print(f'>>>>>>>>>>>>>>>>>        {datetime.datetime.now()}        <<<<<<<<<<<<<<<\n')
    # year = input('Year:  ')
    download_dir = os.path.join(os.getcwd(), "download", "sentenze_cassazione", str(year))
    os.makedirs(download_dir, exist_ok=True)
    os.chmod(download_dir, 0o777)
    local_scrape.get_scrape_list(year)
    