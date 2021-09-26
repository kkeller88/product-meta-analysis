import datetime

import pandas as pd

from product_meta_analysis.database.database import Database
from product_meta_analysis.analyze import tokenize
from product_meta_analysis.utils import read_config


def get_comments(db, category_name):
    query = f"""
        select body, comment_id
        from reddit_comments
        where category = '{category_name}'
        """
    comments = db.read(query)
    return comments

def get_noun_phrases(comments):
    s = tokenize.Tokenizer()
    comments = [
        s.split_and_extract_tokens(x[0])
        for x in comments
        ]
    return comments

def get_brands(tokens, brand_names):
    fbr = brands.FuzzyBrandRecognizer(brands=brand_names)
    brands_ = [fbr.get_brands(x) for x in tokens]
    return brands_

# TODO: This is getting a little messy; can we factor some of this out
def format_data(comments, brands_, brand_names):
    ids = [x[1] for x in comments]
    data = [
        [id, ix, sentence]
        for id, sentences
        in zip(ids, brands_)
        for ix, sentence in enumerate(sentences)
        ]
    data = pd.DataFrame(
        data,
        columns=['comment_id', 'sentence_ix', 'brands']
        )
    data['sentiment'] = 'None'
    data = data.explode('brands')
    brand_names_ = {x:ix for ix, x in enumerate(brand_names)}
    data['brand_ix'] = data['brands'].map(brand_names_)
    data['annotation_id'] = data['comment_id'] + data['sentence_ix'].astype(str) + data['brand_ix'].fillna(-1).astype(int).astype(str)
    data['process_datetime'] = datetime.datetime.now()
    data['process_date'] = datetime.date.today()
    data = data \
        [data['brands'].notnull()] \
        .drop_duplicates(subset=['annotation_id']) \
        .rename(columns={'brands': 'brand'})
    return data

def save_data(data, db):
    data.to_sql(
        name='tmp',
        con=db._con,
        if_exists = 'append',
        index=False
        )
    db.write('INSERT OR IGNORE INTO website_content_annotations SELECT * FROM tmp')
    db.drop('tmp')


config_type = 'reddit_comments'
config_name = 'gluten_free_flour'
config = read_config(config_type, config_name)
brand_names = config.get('brands')
category_name = config.get('name')

db = Database()
comments = get_comments(db, category_name)
tokens = get_noun_phrases(comments)
brands_ = get_brands(tokens, brand_names)
data = format_data(comments, brands_, brand_names)
save_data(data, db)
db.close()
