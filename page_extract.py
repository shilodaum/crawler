import requests
from bs4 import BeautifulSoup as bs
import scrapy
import time
import selenium

# Fields:
# Creators: owner_name
# Title: <meta property="og:title" content="Triple 4K Display Dock for MacBook Pro 2016-2021"/>
# Text (entire html): EZ
# DollarsPledged: total_funds_raised
# DollarsGoal:
# NumBackers:<meta name="sailthru.displayed_contributions" content="2342" />
# DaysToGo: <meta name="sailthru.funding_period" content="standard" />
# and <meta name="sailthru.displayed_days_left" content="25 days left" />
# InDemand <meta name="sailthru.funding_period" content="indemand" />
# FlexibleGoal:"is_fixed_funding":true

main_url = 'https://www.kickstarter.com/discover/categories/technology?page='


def crawl():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/70.0.3538.77 Safari/537.36"}
    address = main_url+"0"

    r = requests.get(address, headers=headers)
    if r.status_code == 200:
        with
        return r.text


def get_fields(html: str):
    driver = webdriver.Firefox()
    driver.get("https://www.indiegogo.com/explore/home?project_type=campaign&project_timing=all&sort=trending")
    print(driver.title)
    elem = driver.find_element_by_name("q")
    elem.clear()
    #e#lem.send_keys("pycon")
    #e#lem.send_keys(Keys.RETURN)
    #assert "No results found." not in driver.page_source
    driver.close()


def main():
    with open("page_exaple.html", 'r') as f:
        h = f.read()
    # h = test_one_web()
    get_fields(h)


if __name__ == '__main__':
    main()
