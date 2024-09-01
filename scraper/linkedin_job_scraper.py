from smart_scraper import CrawlingException

import requests
from bs4 import BeautifulSoup

import logging


logging.basicConfig(level=logging.INFO)


def get_job_post_links(soup):
    job_unordered_list_tag = soup.find("ul", class_="jobs-search__results-list")
    job_link_tags = job_unordered_list_tag.find_all("a", class_="base-card__full-link")

    job_links_list = [job_link_tag.get("href") for job_link_tag in job_link_tags]
    return job_links_list

def get_company_name(soup):
    try:
        company_name = soup.find("a", class_="topcard__org-name-link").text.strip()
    except Exception as error:
        logging.info(f"Error extracting company name from provided web page: {error}")
        company_name = "UNKNOWN"

    return company_name

def get_logo_url(soup):
    try:
        top_card_layout = soup.find("section", class_="top-card-layout")
        logo_url = top_card_layout.find("img", class_="artdeco-entity-image").get("data-delayed-url")
    except Exception as error:
        logging.info(f"Error extracting logo url from provided web page: {error}")
        logo_url = "UNKNOWN"

    return logo_url

def get_posted_ago_in_days(soup):
    try:
        days_posted_ago_in_days = soup.find("span", class_="posted-time-ago__text").text.strip()
    except Exception as error:
        logging.info(f"Error extracting days posted ago information from provided web page: {error}")
        days_posted_ago_in_days = "UNKNOWN"

    return days_posted_ago_in_days

def get_number_of_applicants(soup):
    try:
        number_of_applicants = soup.find(class_="num-applicants__caption").text.strip()
    except Exception as error:
        logging.info(f"Error extracting number of applicatns information from provided web page: {error}")
        number_of_applicants = "UNKNOWN"

    return number_of_applicants

def get_job_title(soup):
    try:
        job_title = soup.find(class_="top-card-layout__title").text.strip()
    except Exception as error:
        logging.info(f"Error extracting job title from provided web page: {error}")
        job_title = "UNKNOWN"

    return job_title

def get_location(soup):
    try:
        location = soup.find(class_="topcard__flavor-row")\
        .find(class_="topcard__flavor--bullet").text.strip()
    except Exception as error:
        logging.info(f"Error extracting location information from provided web page: {error}")
        location = "UNKNOWN"
    
    return location

def get_salary_range(soup):
    try:
        salary_range = soup.find(class_="compensation__salary").text.strip()
    except Exception as error:
        logging.info(f"Error extracting salary information from provided web page: {error}")
        salary_range = "UNKNOWN"
    
    return salary_range

def get_description(soup):
    try:
        description = soup.find(class_="description__text").text.strip()
    except Exception as error:
        logging.info(f"Error extracting job description from provided web page: {error}")
        description = "UNKNOWN"
    
    return description

def get_recruiter_information(soup):
    recruiter_info = {}
    try:
        recruiter_info_tag = soup.find(class_="message-the-recruiter")
        recruiter = recruiter_info_tag.find(class_="base-main-card__title").text.strip()
        recruiter_profile = recruiter_info_tag.find(class_="base-card__full-link").get("href")
        recruiter_position = recruiter_info_tag.find(class_="base-main-card__subtitle").text.strip()
        recruiter_profile_image = recruiter_info_tag.find("img").get("data-delayed-url")

        recruiter_info["recruiter"] = recruiter
        recruiter_info["recruiter_profile"] = recruiter_profile
        recruiter_info["recruiter_position"] = recruiter_position
        recruiter_info["recruiter_profile_image"] = recruiter_profile_image
    except Exception as error:
        logging.info(f"Error extracting job description from provided web page: {error}")

    return recruiter_info

def get_job_criteria(soup):
    job_criteria_dict = {}
    try:
        job_criteria_list_tag = soup.find(class_="description__job-criteria-list")
        job_criteria_list_items = job_criteria_list_tag.find_all("li", class_="description__job-criteria-item")
        for list_item_tag in job_criteria_list_items:
            subheader_tag = list_item_tag.find(class_="description__job-criteria-subheader")
            subheader_text = subheader_tag.text.strip()
            
            description_tag = list_item_tag.find(class_="description__job-criteria-text")
            description_text = description_tag.text.strip()

            job_criteria_dict[subheader_text] = description_text
    except Exception as error:
        logging.info(f"Error extracting job criteria details from provided web page: {error}")
    return job_criteria_dict

def get_benefits(soup):
    benefits_list = []
    benefits_text_tags = soup.find_all(class_="benefit__text")
    for text_tag in benefits_text_tags:
        benefits_list.append(text_tag.text.strip())
    
    return benefits_list


soup_parsing_functions_map = {
    "company": get_company_name,
    "logo_url": get_logo_url,
    "posted_ago_in_days": get_posted_ago_in_days,
    "number_of_applicants": get_number_of_applicants,
    "job_title": get_job_title,
    "location": get_location,
    "salary_range": get_salary_range,
    "description": get_description,
    "recruiter_info": get_recruiter_information,
    "job_criteria": get_job_criteria,
    "benefits": get_benefits
}

def crawl_url(url, headers):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        raise CrawlingException(f"Error crawling, got response code: {response.status_code} - {response.text}")
    
def scrape_linkedin_job_post(job_url, headers):
    job_posting_dict = {}
    job_view_text = crawl_url(job_url, headers)
    job_view_soup = BeautifulSoup(job_view_text, "html.parser")

    job_posting_dict["job_url"] = job_url
    for key, parsing_function in soup_parsing_functions_map.items():
        job_posting_dict[key] = parsing_function(job_view_soup)

    return job_posting_dict
