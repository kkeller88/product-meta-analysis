import datetime
import hashlib
from urllib.parse import urlparse

import pandas as pd

from product_meta_analysis.database.database import Database
import product_meta_analysis.collect.sitemap as s
from product_meta_analysis.utils import read_config


def hash_url(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def standardize_domain(url):
    return urlparse(url).netloc

def get_urls_by_domain(domains):
    urls = [
        [hash_url(url), url, standardize_domain(domain)]
        for domain in domains
        for url in s.extract_urls_from_sitemap(domain)
        ]
    urls = pd.DataFrame(urls, columns=['url_id', 'url', 'domain'])
    urls['process_datetime'] = datetime.datetime.now()
    urls['process_date'] = datetime.date.today()
    return urls

def get_manual_urls(manual_urls):
    urls = [
        [hash_url(url), url, standardize_domain(url)]
        for url in manual_urls
        ]
    urls = pd.DataFrame(urls, columns=['url_id', 'url', 'domain'])
    urls['process_datetime'] = datetime.datetime.now()
    urls['process_date'] = datetime.date.today()
    return urls

def get_urls(domains, manual_urls):
    d = get_urls_by_domain(domains)
    u = get_manual_urls(manual_urls)
    return pd.concat([d,u], axis=0)

def save_urls(data, database):
    data.to_sql(
        name='tmp',
        con=database._con,
        if_exists = 'append',
        index=False
        )
    db.write('INSERT OR IGNORE INTO website_urls SELECT * FROM tmp')
    db.drop('tmp')

config_type = 'website_content'
config_name = 'mac_and_cheese_long'
config = read_config(config_type, config_name)
domains = config.get('urls').get('domains')
manual_urls = config.get('urls').get('urls')

db = Database()
urls = get_urls(domains, manual_urls)
save_urls(urls, db)
db.close()
