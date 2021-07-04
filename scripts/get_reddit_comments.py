import datetime

import pandas as pd

from product_meta_analysis.database import Database
from product_meta_analysis.collect.reddit import Reddit

post_ids = [
    'odm22a'
    ]

# create table
db = Database()
crate_query = f""" CREATE TABLE IF NOT EXISTS reddit_comments (
	id text PRIMARY KEY,
    body text,
    upvotes int,
    parent_id text,
    subreddit text,
    UNIQUE(id)
    )"""
db.write(crate_query)

# get data
def get_comments(post_ids):
    r = Reddit()
    c = [r.get_all_comments_formatted(id) for id in post_ids]
    comments = pd.concat(c)
    return comments
comments = get_comments(post_ids)

# write data
def write_data(data, database):
    data.to_sql(
        name='tmp',
        con=database._con,
        if_exists = 'append',
        index=False
        )
    db.write('INSERT OR IGNORE INTO reddit_comments SELECT * FROM tmp')
    db.drop('tmp')
write_data(comments, db)
