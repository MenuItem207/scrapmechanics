import requests
from bs4 import BeautifulSoup

# a lsit of urls to skip
URLS_TO_AVOID = [
    "https://www.google.com",
    "https://www.youtube.com",
    "https://www.mail.google.com",
    "https://www.twitter.com",
]

# starts from a url and tries to find another domain to scan
def crawl(base_url):
    url_queue = [base_url]
    urls_already_searched = [].extend(URLS_TO_AVOID)
    while url_queue != []:
        url = url_queue.pop(0)
        if url not in urls_already_searched:
            urls_already_searched.append(url)
            other_domains = get_other_domains(url)
            url_queue.extend(other_domains)
            print("searching:" + url + "\ncurrent length: " + str(len(url_queue)))


# scans through a url and finds all the other domains in the url
def get_other_domains(url):
    url_home_page = extract_domain_home_page(url)
    urls = []
    try:
        response = requests.request("GET", url)
        soup = BeautifulSoup(response.text, "lxml")
        for a in soup.find_all("a"):
            possible_link = a.attrs["href"] if "href" in a.attrs else ""
            # if link starts with https://
            # check if link's home page is same as base url
            # if not, add to urls
            if possible_link.startswith("https://"):
                link_home_page = extract_domain_home_page(possible_link)
                if link_home_page != url_home_page and link_home_page not in urls:
                    urls.append("https://" + link_home_page)
    except:
        print("error with " + url)
        return []

    return urls


# takes in https://something.com/something
# and returns something.com
def extract_domain_home_page(url):
    if "https://" in url:
        url = url[8:]

    if "/" in url:
        return url.split("/")[0]
    else:
        return url


print(crawl("http://governmentof.com/singapore/"))
