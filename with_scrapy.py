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
    regex = prefix + variable_reg
    full_row = re.findall(regex, html_txt)
    without_prefix = re.sub(prefix, "", full_row[0])
    idx = without_prefix.find(suffix)
    if idx != -1:
        result = without_prefix[:idx]
    else:
        result = without_prefix[:]
    # result = re.sub(suffix , "", without_prefix)
    # # print(result)
    return result


def get_attributes():
    html_txt_stream = open("item.html", 'rb')
    html_txt = html_txt_stream.read().decode("utf-8")

    # regex for the title:
    # <meta property="og:title" content="Revopoint POP 2: Precise 3D Scanner with 0.1mm Accuracy"/>
    title = find_attribute_by_regex(r"<meta property=\"og:title\" content=\"", r".+", "\"/>", html_txt)
    print('title =', title)

    # regex for the creator
    # <div class="type-14 bold clip ellipsis"> Revopoint 3D </div><div class="mr2">
    creator = find_attribute_by_regex(r"<div class=\"type-14 bold clip ellipsis\">", r".+", "</div><div class=\"mr2\">", html_txt)
    print('creator = ', creator)

    # Text (entire html)
    text = html_txt

    # DollarsPledged
    DollarsPledged = find_attribute_by_regex(r"converted_pledged_amount&quot;:", r"[0-9]+", ",", html_txt)
    print('DollarsPledged =', DollarsPledged)

    # DollarGoal
    DollarGoal = find_attribute_by_regex(r"\"project_goal_usd\":", r'[0-9]+\.?[0-9]+', ",", html_txt)
    print('DollarGoal =', DollarGoal)

    # NumBackers
    NumBackers = find_attribute_by_regex(r"backers_count&quot;:", r"[0-9]+", ",", html_txt)
    print('NumBackers =', NumBackers)

    # DaysToGo
    DaysToGo = find_attribute_by_regex(r"<span class=\"block type-16 type-28-md bold dark-grey-500\">", r"[0-9]+",
                                       "</span>", html_txt)
    print('DaysToGo =', DaysToGo)

    # AllOrNothing
    AllOrNothing = find_attribute_by_regex(r"<span data-test-id=\"deadline-exists\">", r".*", "</span>", html_txt)
    print('AllOrNothing = ', AllOrNothing)


if __name__ == '__main__':
    # download_file()
    get_attributes()
