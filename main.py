
import updated_scrape
import upload
import time

if __name__ == "__main__":
    # while True:
    updated_scrape.ScrapeList(2010, 2025)
    upload.UploadPdf()
        # time.sleep(10)
        