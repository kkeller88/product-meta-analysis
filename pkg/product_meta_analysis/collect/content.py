import requests

from bs4 import BeautifulSoup

#url = "https://cookieandkate.com/tag/acorn-squash/"
url = "https://cookieandkate.com/spicy-squash-soup-recipe/"
response = requests.get(url).text
soup = BeautifulSoup(response, 'html.parser')
print(soup.prettify())

printitems)
