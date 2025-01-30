
import updated_scrape
# import upload
import time
import sys


if __name__ == "__main__":
    start = input("Start year: ")
    end = input("End year: ")
    
    # while True:
    updated_scrape.ScrapeList(int(start), int(end))
    # upload.UploadPdf()
        # time.sleep(10)
        