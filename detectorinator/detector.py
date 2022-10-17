import requests
from bs4 import BeautifulSoup

link = "INSERTLINKHERE"
response = requests.request("GET", link)
soup = BeautifulSoup(response.text, "lxml")
print(soup)
