import pandas as pd

from product_meta_analysis.database import Database
from product_meta_analysis.analyze import tokenize
from product_meta_analysis.analyze import brands
from product_meta_analysis.utils import read_config

# TODO: Long term we should identiy brands based on text
file_name = 'gluten_free_flour'

# get comments
db = Database()
query = f"""
    select body, id
    from reddit_comments
    where category = 'gluten_free_flour'
    limit 20
    """
comments = db.read(query)

# tokenize comments
def get_noun_phrases(comments):
    s = tokenize.Tokenizer()
    comments = [
        s.split_and_extract_tokens(x[0])
        for x in comments
        ]
    return comments
tokens = get_noun_phrases(comments)

# identify brands
def get_brands(tokens, brand_names):
    fbr = brands.FuzzyBrandRecognizer(brands=brand_names)
    brands_ = [fbr.get_brands(x) for x in tokens]
    return brands_
brand_names = read_config('reddit_comments', file_name).get('brands')
brands_ = get_brands(tokens, brand_names)

# format data
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
    return data
data = format_data(comments, brands_, brand_names)
print(data)


# load data
def load_data(data, db):
    crate_query = f""" CREATE TABLE IF NOT EXISTS reddit_comment_annotations (
    	id text,
        sentence_ix int,
        brands text,
    	sentiment text,
        brand_ix int,
        annotation_id text PRIMARY KEY,
        UNIQUE(annotation_id)
        )"""
    db.write(crate_query)

    data.to_sql(
        name='tmp',
        con=db._con,
        if_exists = 'append',
        index=False
        )
    db.write('INSERT OR IGNORE INTO reddit_comment_annotations SELECT * FROM tmp')
    db.drop('tmp')

db = Database()
load_data(data, db)
