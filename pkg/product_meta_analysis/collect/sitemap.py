import os

from bs4 import BeautifulSoup
import requests


def construct_sitemap_url(home):
    return os.path.join(home, 'sitemap.xml')

def get_page_urls(url):
    print(f'Extracting page urls from {url}')
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    urls = [element.text for element in soup.findAll('loc')]
    return urls

def get_sitemap_urls(url):
    print(f'Extracting sitemap urls from {url}')
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    sitemapTags = soup.find_all("sitemap")
    sitemaps = [sitemap.findNext("loc").text for sitemap in sitemapTags]
    return sitemaps

def extract_urls_from_sitemap(home):
    url = construct_sitemap_url(home)
    sitemap_urls = get_sitemap_urls(url)
    if len(sitemap_urls) == 0:
        page_urls = get_page_urls(url)
    else:
        page_urls = []
        for sitemap_url in sitemap_urls:
            page_urls_ = get_page_urls(sitemap_url)
            page_urls.extend(page_urls_)
    return page_urls
