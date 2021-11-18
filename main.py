import requests
import bs4
import scrapy
import time

def test_one_web():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/70.0.3538.77 Safari/537.36"}
    adress='https://www.indiegogo.com/projects/triple-4k-display-dock-for-macbook-pro-2016-2021#/'
    r = requests.get(adress, headers=headers)

    print(r.status_code)
    print(r.text)


if __name__ == '__main__':
    test_one_web()
