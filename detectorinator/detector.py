import requests
from bs4 import BeautifulSoup

# takes in a link and extracts the relevant data
def extract(link):
    response = requests.request("GET", link)
    soup = BeautifulSoup(response.text, "lxml")

    return {
        "url": link,
        "is_ip_address": link_has_at(link),
        "has_at": link_has_at(link),
        "has_dash": link_has_dash(link),
    }


# links that are ip addresses are kinda sus
# returns 1 if is ip address and 0 if not
def link_is_ip_address(link):
    # extract the home-page link first, assumes link starts with https:// or http://

    # remove https://
    if link.startswith("https://"):
        link = link[8:]

    # remove http://
    elif link.startswith("http://"):
        link = link[7:]

    # only keep the first part of link i.e www.google.com/a becomes www.google.com
    if "/" in link:
        link = link.split("/")[0]

    # remove all dots, i.e www.google.com becomes wwwgooglecom
    link = link.replace(".", "")

    # check if can be converted to int, if so is ip address
    try:
        int(link)
        return 1
    except:
        return 0


# using the @ symbol leads the browser to ignore everything preceding it
# returns 1 if has @ and 0 if not
def link_has_at(link):
    return 1 if "@" in link else 0


# the use of "-" is rarely use in legit urls
# returns 1 if has @ and 0 if not
def link_has_dash(link):
    return 1 if "-" in link else 0


link = "http://www.google.com"
print(extract(link))
