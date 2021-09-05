import datetime
import hashlib

import pandas as pd

from product_meta_analysis.database.database import Database
import product_meta_analysis.collect.sitemap as s

domains = [
    "https://helpmecleanthis.com/",
    #"https://glutenfreeonashoestring.com/",
    ]

def hash_url(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def get_urls(domains):
    urls = [
        [hash_url(url), url, domain]
        for domain in domains
        for url in s.extract_urls_from_sitemap(domain)
        ]
    urls = pd.DataFrame(urls, columns=['url_id', 'url', 'domain'])
    urls['process_datetime'] = datetime.datetime.now()
    urls['process_date'] = datetime.date.today()
    return urls

def save_urls(data, database):
    data.to_sql(
        name='tmp',
        con=database._con,
        if_exists = 'append',
        index=False
        )
    db.write('INSERT OR IGNORE INTO website_urls SELECT * FROM tmp')
    db.drop('tmp')

db = Database()
urls = get_urls(domains)
save_urls(urls, db)
db.close()
