from celery import Celery

from smart_scraper import SmartScraper
from linkedin_job_scraper import scrape_linkedin_job_post


app = Celery(
    'scalable_smart_scraper',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

# TODO:
# 1. How to allow parallel tasks, look into delay more
# 2. Is it possible to distribute tasks across different celery workers across different machines?

@app.task
def smart_scrape(url):
    scraper = SmartScraper(scrape_linkedin_job_post, url)
    data = scraper.execute()
    return data
