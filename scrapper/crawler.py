import requests
from bs4 import BeautifulSoup

# a lsit of urls to skip
URLS_TO_AVOID = [
    "https://www.google.com",
    "https://www.youtube.com",
    "https://www.mail.google.com",
    "https://www.twitter.com",
    "https://youtube.com",
    "https://facebook.com",
    "https://twitter.com",
    "https://instagram.com",
    "https://www.linkedin.com",
    "https://developers.google.com",
    "https://www.facebook.com",
    "https://developers.facebook.com",
    "https://developer.linkedin.com",
    "https://translate.google.com",
    "https://www.google.com.sg",
    "https://accounts.google.com",
    "https://policies.google.com",
    "https://support.google.com",
    "https://cloud.google.com",
    "https://maps.google.com.sg",
    "https://play.google.com",
    "https://news.google.com",
    "https://mail.google.com",
    "https://drive.google.com",
    "https://myaccount.google.com",
    "https://safety.google",
    "https://account.google.com",
    "https://about.google",
    "https://firebase.google.com",
    "https://payments.google.com",
    "https://developer.apple.com",
]

# starts from a url and tries to find another domain to scan
def crawl(base_url):
    url_queue = [base_url]
    urls_already_searched = URLS_TO_AVOID
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
        response = requests.request("GET", url, timeout=30)  # max 30s
        soup = BeautifulSoup(response.text, "lxml")
        for a in soup.find_all("a"):
            possible_link = a.attrs["href"] if "href" in a.attrs else ""
            # if link starts with https:// or http://
            # check if link's home page is same as base url
            # if not, add to urls
            if possible_link.startswith("https://") or possible_link.startswith(
                "http://"
            ):
                link_home_page = extract_domain_home_page(possible_link)
                if link_home_page != url_home_page and link_home_page not in urls:
                    urls.append(link_home_page)
    except:
        print("error with " + url)
        return []

    return urls


# takes in https://something.com/something
# and returns https://something.com
def extract_domain_home_page(url):
    # remove https:// or http://
    linkPrefix = ""
    if "https://" in url:
        url = url[8:]
        linkPrefix = "https://"

    if "http://" in url:
        url = url[7:]
        linkPrefix = "http://"

    # remove extra /
    if "/" in url:
        return linkPrefix + url.split("/")[0]
    else:
        return linkPrefix + url


print(crawl("http://governmentof.com/singapore/"))