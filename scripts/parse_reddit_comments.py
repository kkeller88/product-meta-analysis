import datetime

import pandas as pd

from product_meta_analysis.database.database import Database
from product_meta_analysis.analyze import tokenize
from product_meta_analysis.analyze import brands
from product_meta_analysis.utils import read_config


def get_comments(db, file_name):
    query = f"""
        select body, id
        from reddit_comments
        where category = '{file_name}'
        limit 20
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
        columns=['id', 'sentence_ix', 'brands']
        )
    data['sentiment'] = 'None'
    data = data.explode('brands')
    brand_names_ = {x:ix for ix, x in enumerate(brand_names)}
    data['brand_ix'] = data['brands'].map(brand_names_)
    data['annotation_id'] = data['id'] + data['sentence_ix'].astype(str) + data['brand_ix'].fillna(-1).astype(int).astype(str)
    data['process_datetime'] = datetime.datetime.now()
    data['process_date'] = datetime.date.today()
    data = data \
        [data['brands'].notnull()] \
        .drop_duplicates(subset=['annotation_id'])
    return data

def save_data(data, db):
    data.to_sql(
        name='tmp',
        con=db._con,
        if_exists = 'append',
        index=False
        )
    db.write('INSERT OR IGNORE INTO reddit_comment_annotations SELECT * FROM tmp')
    db.drop('tmp')


file_name = 'gluten_free_flour'
config_name = 'reddit_comments'

# TODO: Long term we should identiy brands based on text
brand_names = read_config(config_name, file_name).get('brands')

db = Database()
comments = get_comments(db, file_name)
tokens = get_noun_phrases(comments)
brands_ = get_brands(tokens, brand_names)
data = format_data(comments, brands_, brand_names)
save_data(data, db)
db.close()
