import datetime

import pandas as pd

from product_meta_analysis.database import Database
import product_meta_analysis.collect.sitemap as s

sites = {
    #"glutenfreeonashoestring": "https://glutenfreeonashoestring.com/",
    #"glutenfreepalate": "https://www.glutenfreepalate.com/"
    }


# create table
db = Database()
crate_query = f""" CREATE TABLE IF NOT EXISTS urls (
	url text PRIMARY KEY,
	site text NOT NULL,
    UNIQUE(url)
    )"""
db.write(crate_query)

# get data
def format_data(name, url):
    urls = s.extract_urls_from_sitemap(url)
    return pd.DataFrame({
        "url": urls,
        "site":[name]*len(urls)
        })
urls = [format_data(k, v) for k, v in sites.items()]

# write data
def write_data(data, database):
    data.to_sql(
        name='tmp',
        con=database._con,
        if_exists = 'append',
        index=False
        )
    db.write('INSERT OR IGNORE INTO urls SELECT * FROM tmp')
    db.drop('tmp')
[write_data(x, db) for x in urls]
