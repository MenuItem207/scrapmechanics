import requests
from bs4 import BeautifulSoup

# takes in a link and extracts the relevant data
def extract(link):
    response = requests.request("GET", link)
    soup = BeautifulSoup(response.text, "lxml")

    return {
        "url": link,
        "has_at": link_has_at(link),
        "has_dash": link_has_dash(link),
    }


# using the @ symbol leads the browser to ignore everything preceding it
# returns 1 if has @ and 0 if not
def link_has_at(link):
    return 1 if "@" in link else 0


# the use of "-" is rarely use in legit urls
# returns 1 if has @ and 0 if not
def link_has_dash(link):
    return 1 if "-" in link else 0


link = "https://insert_link_here"
print(extract(link))
