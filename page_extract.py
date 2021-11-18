import requests
from bs4 import BeautifulSoup as bs
import scrapy
import time
import selenium
import re
import json

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

def find_attribute_by_regex(prefix, variable_reg, suffix, html_txt):
    regex = prefix + variable_reg + suffix
    full_row = re.findall(regex, html_txt)
    without_prefix = re.sub(prefix, "", full_row[0])
    idx = without_prefix.find(suffix)
    result = without_prefix[:idx]
    # result = re.sub(suffix , "", without_prefix)
    # # print(result)
    return result


def get_attributes(html_txt):
    # html_txt_stream = open("item.html", 'rb')
    # html_txt = html_txt_stream.read()
    html_txt=html_txt.decode("utf-8")

    attr=dict()
    # regex for the title:
    # <meta property="og:title" content="Revopoint POP 2: Precise 3D Scanner with 0.1mm Accuracy"/>
    title = find_attribute_by_regex(r"<meta property=\"og:title\" content=\"", r".+", r"\"/>", html_txt)
    print('title =', title)

    attr['title']=title
    # regex for the creator
    #
    creator = find_attribute_by_regex(r"<div class=\"type-14 bold clip ellipsis\">", r".+", "</div><div class=\"mr2\">", html_txt)
    print('creator = ', creator)

    attr['creator']=creator


    # Text (entire html)
    text = html_txt

    #TODO add this line
    #attr['text']=text
    # DollarsPledged
    # converted_pledged_amount&quot;:617454,
    DollarsPledged = find_attribute_by_regex(r"converted_pledged_amount&quot;:", r"[0-9]+", r",", html_txt)
    print('DollarsPledged =', DollarsPledged)

    attr['DollarsPledged']=DollarsPledged

    # DollarGoal
    # "project_goal_usd":9975.29,
    DollarGoal = find_attribute_by_regex(r"\"project_goal_usd\":", r'[0-9]+\.?[0-9]+', r",", html_txt)
    print('DollarGoal =', DollarGoal)

    attr['DollarGoal']=DollarGoal


    # NumBackers
    # backers_count&quot;:1341,&quot;
    NumBackers = find_attribute_by_regex(r"backers_count&quot;:", r"[0-9]+", r",", html_txt)
    print('NumBackers =', NumBackers)

    attr['NumBackers']=NumBackers


    # DaysToGo
    # <span class="block type-16 type-28-md bold dark-grey-500"> #### </span>
    DaysToGo = find_attribute_by_regex(r"<span class=\"block type-16 type-28-md bold dark-grey-500\">", r"[0-9]+",
                                       r"</span>", html_txt)
    print('DaysToGo =', DaysToGo)

    attr['DaysToGo']=DaysToGo

    # AllOrNothing
    # <span data-test-id="deadline-exists"> ### This project will only be funded if it reaches its goal by Sat, January 1 2022 3:00 PM UTC +02:00. ### </span>
    AllOrNothing = find_attribute_by_regex(r"<span data-test-id=\"deadline-exists\">", r".*", r"</span>", html_txt)
    print('AllOrNothing = ', AllOrNothing)

    attr['AllOrNothing']=AllOrNothing

    return attr


def crawl():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/70.0.3538.77 Safari/537.36"}

    for i in range(25):
        address = main_url + str(i)
        r = requests.get(address, headers=headers)
        if r.status_code == 200:
            with open(f"menus/menu{i}.html", "wb") as f:
                f.write(r.content)
            links = get_links(r.content)
            j = 0
            with open(f'menus/menu{i}.json', 'w') as fj:
                json.dump(links, fj)
            for link in links:

                time.sleep(5)
                file_index = i * 12 + j
                print(file_index)
                j += 1
                r1 = requests.get(link, headers=headers)
                if r1.status_code == 200:
                    with open(f"files/file{file_index}.html", "wb") as f:
                        f.write(r1.content)


def get_links(html):
    soup = bs(html, 'html.parser')
    divs = soup.find_all('div', attrs={"class": "js-react-proj-card grid-col-12 grid-col-6-sm grid-col-4-lg"})
    links = list()
    for div in divs:
        tag = str(div)
        start_of_link = tag[tag.find("https://www.kickstarter.com/projects/"):]
        link = start_of_link[:start_of_link.find('"')]
        if link.find('&') != -1:
            link = link[:link.find('&')]
        links.append(link)
    return links

    # print(str(i)[str(i).find("https://www.kickstarter.com/projects/"):])
    # y = re.search("https://www\.kickstarter\.com/projects/.*;", str(i))
    # print(y)


def fill_json():
    urls = list()
    with open("menus/menu.json", "r") as f:
        urls = json.load(f)

    record = list()

    for i in range(300):
        with open(f'files/file{i}.html', "rb") as f:
            attr = get_attributes(f.read())
            attr['id'] = str(i)
            attr['url'] = urls[i]
            record.append(attr)

    dict_dataset = dict()
    dict_dataset['records'] = {'record': record}

    with open("dataset.json", 'w') as f:
        json.dump(dict_dataset, f)


def make_one_menu():
    menu_list = list()
    for i in range(25):
        with open(f"menus/menu{i}.json", "r") as f:
            menu_list = menu_list + json.load(f)

        with open("menus/menu.json", 'w') as m:
            json.dump(menu_list, m)


def main():
    make_one_menu()


if __name__ == '__main__':
    fill_json()
