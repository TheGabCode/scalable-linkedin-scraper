import logging
import time

logging.basicConfig(level=logging.INFO)


class CrawlingException(Exception):
    pass

class SmartScraper:
    # TODO:
    # [DONE] 1. Retries, exponential backoff 
    # 2. Proxy IP Rotation, implement tries per proxy? e.g. give each proxy 5 tries before rotating, how many times can we rotate proxy?
    # 3. User-Agent Rotation

    def __init__(self, scraping_function, url, max_retries=3):
        self.url = url
        self.headers = {}
        self.scraping_function = scraping_function
        self.max_retries = max_retries
        self.BASE_TIMEOUT_SECONDS = 1
        self.BACKOFF_FACTOR = 2


    def exponential_backoff_sleep(self, attempt):
            pause_in_seconds = self.BASE_TIMEOUT_SECONDS * (self.BACKOFF_FACTOR ** attempt)
            logging.info(f"Sleeping for {pause_in_seconds} seconds...")
            time.sleep(pause_in_seconds)


    def execute(self):
        attempts = 0
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        self.headers = {'User-Agent': user_agent}

        data = {}
        while attempts < self.max_retries:
            try:
                data = self.scraping_function(self.url, self.headers)
                break               
            except CrawlingException as error:
                logging.info(f"[Attempt {attempts+1}/{self.max_retries}] Error encountered crawling {self.url}: {error}")
                attempts += 1
                self.exponential_backoff_sleep(attempts)

        return data
