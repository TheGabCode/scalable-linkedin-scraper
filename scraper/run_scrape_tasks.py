from scraper_celery_app import smart_scrape

import json

# TODO: Initial scraping of job list
URL_LIST = [
    "https://www.linkedin.com/jobs/view/private-equity-associate-at-blacklock-financial-4000484231?position=2&pageNum=0&refId=hCDcw%2BDzFlfBt4UtoWeodw%3D%3D&trackingId=pY%2FOQUSvRzp96Rj2FskwFg%3D%3D&trk=public_jobs_jserp-result_search-card",
    "https://www.linkedin.com/jobs/view/%2420-hr-crew-member-west-linn-at-killer-burger-4000457170?position=3&pageNum=0&refId=hCDcw%2BDzFlfBt4UtoWeodw%3D%3D&trackingId=IkfGT6ox6ahxuKgXO9JOMw%3D%3D&trk=public_jobs_jserp-result_search-card",
    "https://www.linkedin.com/jobs/view/2d-artist-at-playnetic-4000477505?position=4&pageNum=0&refId=hCDcw%2BDzFlfBt4UtoWeodw%3D%3D&trackingId=4GUZHnp9sFuMlvKYqmsdNQ%3D%3D&trk=public_jobs_jserp-result_search-card"
]

job_data = []
for url in URL_LIST:
    result = smart_scrape.delay(url)
    job_data.append(result.get())

with open('output/jobs.json', 'w') as fout:
    json.dump(job_data, fout, indent=4)