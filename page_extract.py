import requests
from bs4 import BeautifulSoup as bs
import time
import re
import json
import os

SLEEPING_TIME = 5
main_url = 'https://www.kickstarter.com/discover/categories/technology?page='

def initial():
    """
    Creates the folders 'menus' and 'files'
    """
    # Create the pages folder
    if not os.path.isdir('menus'):
        os.mkdir('menus')

    # Create the components folder
    if not os.path.isdir('files'):
        os.mkdir('files')


def crawl():
    """
    Do crawling on the pages in main_url and download them.
    """

    # Create the headers dict to get the HTML main page
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "}
    # Run on 25 pages in the html of the website
    for i in range(25):

        # Create the address of the current page
        address = main_url + str(i)
        r = requests.get(address, headers=headers)

        # If the request succeeded
        if r.status_code == 200:
            print(f'menu{i}')

            # Download the current page HTML
            with open(f"menus/menu{i}.html", "wb") as f:
                f.write(r.content)

            # Create list of the components links in the current page
            links = get_links(r.content)

            # Create JSON file to the page that includes the components links
            with open(f'menus/menu{i}.json', 'w') as fj:
                json.dump(links, fj)

            comp_idx = 0
            # Get the HTML page of each component in the current page
            for link in links:

                # Wait SLEEPING_TIME between each reading
                time.sleep(SLEEPING_TIME)

                # In each page there are 12 components. Here we calculate the index of the current component page
                file_index = i * 12 + comp_idx
                comp_idx += 1

                # Print the component index for progress checking
                print(file_index)

                r1 = requests.get(link, headers=headers)

                # Download the HTML file of each component
                if r1.status_code == 200:
                    with open(f"files/file{file_index}.html", "wb") as f:
                        f.write(r1.content)


def get_links(html):
    """
    Extract a list of links of the components of the current HTML page (= one menu)

    :param html: The content of HTML file
    :return: A list of the links of the page's components
    """

    # Find the divs which contain the links
    soup = bs(html, 'html.parser')
    divs = soup.find_all('div', attrs={"class": "js-react-proj-card grid-col-12 grid-col-6-sm grid-col-4-lg"})
    links = list()

    # For each div isolate the link
    for div in divs:
        tag = str(div)

        # Find the link by cutting the prefix and the suffix of the tag
        start_of_link = tag[tag.find("https://www.kickstarter.com/projects/"):]
        link = start_of_link[:start_of_link.find('"')]

        # Some links end with &
        if link.find('&') != -1:
            link = link[:link.find('&')]

        links.append(link)

    return links


def make_one_menu():
    """
    Merge the menus of each page into one json file
    """

    menu_list = list()
    for i in range(25):
        with open(f"menus/menu{i}.json", "r") as f:
            menu_list = menu_list + json.load(f)

        with open("menus/menu.json", 'w') as m:
            json.dump(menu_list, m)


def fill_json():
    """
    Fill the json file of each HTML component file
    """

    # Get the links of the components
    urls = list()
    with open("menus/menu.json", "r") as f:
        urls = json.load(f)

    record = list()

    # Run over all of the components
    for i in range(300):

        # Open the component HTML file
        with open(f'files/file{i}.html', "rb") as f:
            attr = get_attributes(f.read())
            attr['id'] = str(i)
            attr['url'] = urls[i]

            # Append the attributes dictionary of the current component to the final result
            record.append(attr)

    dict_dataset = dict()
    dict_dataset['records'] = {'record': record}

    # Download the final result as a JSON file
    with open("dataset.json", 'w') as f:
        json.dump(dict_dataset, f)


def get_attributes(html_content):
    """
    Returns the required attributes of the given component
    :param html_content: The content of HTML component
    :return: attributes dictionary
    """

    html_txt = html_content.decode("utf-8")

    attr = dict()

    # Get the title attribute
    title = find_attribute_by_regex(r"<meta property=\"og:title\" content=\"", r".+", "\"/>", html_txt)
    attr['title'] = title

    # Get the creator attribute
    creator = find_attribute_by_regex(r"<div class=\"type-14 bold clip ellipsis\">", r".+", "</div><div class=\"mr2\">",
                                      html_txt)
    attr['creator'] = creator

    # Get the text attribute
    text = html_txt

    # TODO correct this line
    # attr['text'] = text

    # Get the DollarsPledged attribute
    DollarsPledged = find_attribute_by_regex(r"converted_pledged_amount&quot;:", r"[0-9]+", ",", html_txt)
    attr['DollarsPledged'] = DollarsPledged

    # Get the DollarGoal attribute
    DollarGoal = find_attribute_by_regex(r"\"project_goal_usd\":", r'[0-9]+\.?[0-9]+', ",", html_txt)
    attr['DollarGoal'] = DollarGoal

    # Get the NumBackers attribute
    NumBackers = find_attribute_by_regex(r"backers_count&quot;:", r"[0-9]+", ",", html_txt)
    attr['NumBackers'] = NumBackers

    # Get the DaysToGo attribute
    DaysToGo = find_attribute_by_regex(r"<span class=\"block type-16 type-28-md bold dark-grey-500\">", r"[0-9]+",
                                       "</span>", html_txt)
    attr['DaysToGo'] = DaysToGo

    # Get the AllOrNothing attribute
    # TODO correct this line
    AllOrNothing = find_attribute_by_regex(r"<span data-test-id=\"deadline-exists\">", r".*", "</span>", html_txt)
    attr['AllOrNothing'] = AllOrNothing

    return attr


def find_attribute_by_regex(prefix, variable_reg, suffix, html_txt):
    """
    Find the attribute in the HTML text file

    :param prefix: Regex of the attribute prefix
    :param variable_reg: Regex of the attribute
    :param suffix: String of the suffix
    :param html_txt: HTML file text
    :return: Required attribute
    """

    # Build a regex of the prefix and the attribute
    regex = prefix + variable_reg

    # Find the the regex content with suffix and prefix
    full_row = re.findall(regex, html_txt)

    # remove the prefix and the suffix
    without_prefix = re.sub(prefix, "", full_row[0])
    idx = without_prefix.find(suffix)
    if idx != -1:
        result = without_prefix[:idx]
    else:
        result = without_prefix[:]

    return result


if __name__ == '__main__':
    initial()
    crawl()
    make_one_menu()
    fill_json()