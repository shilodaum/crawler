import requests
from bs4 import BeautifulSoup
import re


def download_file():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/70.0.3538.77 Safari/537.36"}
    address = 'https://www.kickstarter.com/projects/2125914059/revopoint-pop2-high-precision-3d-scanner?ref=discovery_category'
    r = requests.get(address, headers=headers)
    with open("item.html", 'wb') as f:
        f.write(r.content)


def find_attribute_by_regex(prefix, variable_reg, suffix, html_txt):
    regex = prefix + variable_reg + suffix
    full_row = re.findall(regex, html_txt)
    without_prefix = re.sub(prefix, "", full_row[0])
    idx = without_prefix.find(suffix)
    result = without_prefix[:idx]
    # result = re.sub(suffix , "", without_prefix)
    # # print(result)
    return result


def get_attributes():
    html_txt_stream = open("item.html", 'rb')
    html_txt = html_txt_stream.read().decode("utf-8")

    # regex for the title:
    # <meta property="og:title" content="Revopoint POP 2: Precise 3D Scanner with 0.1mm Accuracy"/>
    title = find_attribute_by_regex(r"<meta property=\"og:title\" content=\"", r".+", r"\"/>", html_txt)
    print('title =', title)

    # regex for the creator
    #

    # Text (entire html)
    text = html_txt

    # DollarsPledged
    # converted_pledged_amount&quot;:617454,
    DollarsPledged = find_attribute_by_regex(r"converted_pledged_amount&quot;:", r"[0-9]+", r",", html_txt)
    print('DollarsPledged =', DollarsPledged)

    # DollarGoal
    # "project_goal_usd":9975.29,
    DollarGoal = find_attribute_by_regex(r"\"project_goal_usd\":", r'[0-9]+\.?[0-9]+', r",", html_txt)
    print('DollarGoal =', DollarGoal)

    # NumBackers
    # backers_count&quot;:1341,&quot;
    NumBackers = find_attribute_by_regex(r"backers_count&quot;:", r"[0-9]+", r",", html_txt)
    print('NumBackers =', NumBackers)

    # DaysToGo
    # <span class="block type-16 type-28-md bold dark-grey-500"> #### </span>
    DaysToGo = find_attribute_by_regex(r"<span class=\"block type-16 type-28-md bold dark-grey-500\">", r"[0-9]+",
                                       r"</span>", html_txt)
    print('DaysToGo =', DaysToGo)

    # AllOrNothing
    # <span data-test-id="deadline-exists"> ### This project will only be funded if it reaches its goal by Sat, January 1 2022 3:00 PM UTC +02:00. ### </span>
    AllOrNothing = find_attribute_by_regex(r"<span data-test-id=\"deadline-exists\">", r".*", r"</span>", html_txt)
    print('AllOrNothing = ', AllOrNothing)


def new():
    url = "https://www.rottentomatoes.com/top/bestofrt/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    f = requests.get(url, headers=headers)

    movies_lst = []

    soup = BeautifulSoup(f.content, 'lxml')
    movies = soup.find('table', {
        'class': 'table'}).find_all('a')

    num = 0
    for anchor in movies:
        urls = 'https://www.rottentomatoes.com' + anchor['href']

    movies_lst.append(urls)
    num += 1
    movie_url = urls
    movie_f = requests.get(movie_url, headers=headers)
    movie_soup = BeautifulSoup(movie_f.content, 'lxml')
    movie_content = movie_soup.find('div', {
        'class': 'movie_synopsis clamp clamp-6 js-clamp'
    })
    print(num, urls, '\n', 'Movie:' + anchor.string.strip())
    print('Movie info:' + movie_content.string.strip())


if __name__ == '__main__':
    # download_file()
    get_attributes()
