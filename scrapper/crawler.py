import requests
from bs4 import BeautifulSoup
from pathlib import Path

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
    urls = []
    try:
        response = requests.request("GET", url, timeout=30)  # max 30s
        soup = BeautifulSoup(response.text, "lxml")
        for a in soup.find_all("a"):
            possible_link = a.attrs["href"] if "href" in a.attrs else ""
            final_subdomain = get_final_subdomain(possible_link)
            # if link starts with https:// or http:// and has no suffix (prevent downloading)
            if (
                possible_link.startswith("https://")
                or possible_link.startswith("http://")
            ) and not Path(final_subdomain).suffix:
                # check if link's is same as base url
                # if not, add to urls
                if possible_link != url and possible_link not in urls:
                    urls.append(possible_link)
    except:
        print("error with " + url)
        return []

    return urls


# takes in https://www.google.com/a/b and returns b
def get_final_subdomain(url):
    # remove https:// or http://
    if "https://" in url:
        url = url[8:]

    if "http://" in url:
        url = url[7:]

    # has subdomains
    if "/" in url:
        # if last character is a / then remove it and check again
        if url[-1] == "/":
            url = url.rstrip(url[-1])
            if "/" not in url:
                return ""

        return url.split("/")[-1]
    else:
        return ""


print(crawl("http://governmentof.com/singapore/"))
