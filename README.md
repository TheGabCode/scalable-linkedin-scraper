# scalable-linkedin-scraper
Scalable Linkedin job post scraping

#### Tech Stack
1. BeautifulSoup
2. Redis
3. Celery

#### Prerequisites
1. nix-shell

#### Setup
Run the following commands:
1. nix-shell nix/default.nix
2. python main.py

#### TODO:
1. Distributed crawling via Celery 
2. Proxy Management/IP Rotation
3. User-Agent Management
4. Set up lints