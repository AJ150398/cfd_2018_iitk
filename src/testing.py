def f():
    rate = 0.5
    rate = str(rate)
    print("Negative Reviews!! Drop this Movie" + "rating is : " + rate)
f()

"""
title = "black panther"

new_title = title.replace(" ", "_")  # to be able to use it in the url
my_url = "https://www.rottentomatoes.com/m/" + new_title + "/reviews/"

print(my_url)

import requests
from bs4 import BeautifulSoup

req = requests.get(my_url)
content = req.content
soup = BeautifulSoup(content, "html.parser")
element = soup.find_all("div", {"class": "the_review"})

if len(element) == 0:
    new_url = req.url + "/reviews/"
    req = requests.get(new_url)
    content = req.content
    soup = BeautifulSoup(content, "html.parser")
    element = soup.find_all("div", {"class": "the_review"})

print(element)
"""