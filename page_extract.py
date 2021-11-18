import requests
import bs4
import scrapy
import time

def extract_fields_from_html(html):
    fields=['owner_name',]

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

main_url='https://www.indiegogo.com/explore/home?project=all&project=all&sort=trending'

def test_one_web():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/70.0.3538.77 Safari/537.36"}
    adress=main_url
    r = requests.get(adress, headers=headers)
    with open("itemlist.html",'w') as f:
        f.write(r.text)
test_one_web()