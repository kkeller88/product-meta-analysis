import json
import datetime

import pandas as pd

from product_meta_analysis.database.database import Database
from product_meta_analysis.utils import read_config
from product_meta_analysis.analyze import brands


def get_data(db):
    query = """
        select
            url_id,
            content_type,
            content
        from website_content
        where content_type = 'schema_recipe_card_ingredients'
            and content is not null
        """
    content = db.read(query)
    data = pd.DataFrame(content, columns=['url_id', 'content_type', 'content'])
    data['ingredients'] = [
        [i.get('full_text') for i in json.loads(ingredients)]
        for ingredients in data['content']
        ]
    return data

def get_matches(data, match_terms):
    def match_single_item(ingredients, match_terms):
        ingredients_ = ' ; '.join(ingredients).lower()
        matches = [x for x in match_terms if x.lower() in ingredients_]
        return matches

    data['matched_ingredients'] = [
        match_single_item(x, match_terms)
        for x in data['ingredients']
        ]
    return data

def format_data(data, match_terms):
    cols = ['url_id', 'content_type', 'sentence_ix', 'annotation',
        'annotation_ix', 'sentiment', 'annotation_id', 'process_datetime',
        'process_date']
    data = data \
        .explode('matched_ingredients') \
        .rename(columns={'matched_ingredients':'annotation'})
    data['sentiment'] = 'None'
    data['sentence_ix'] = 0
    match_indicies = {x:ix for ix, x in enumerate(match_terms)}
    data['annotation_ix'] = data['annotation'].map(match_indicies)
    data['process_datetime'] = datetime.datetime.now()
    data['process_date'] = datetime.date.today()
    data['annotation_id'] = data['url_id'] + data['sentence_ix'].astype(str) + data['annotation_ix'].fillna(-1).astype(int).astype(str)
    data = data \
        [data['annotation'].notnull()] \
        .drop_duplicates(subset=['annotation_id'])
    return data[cols]

def save_data(data, db):
    data.to_sql(
        name='tmp',
        con=db._con,
        if_exists = 'append',
        index=False
        )
    db.write('INSERT OR IGNORE INTO website_content_annotations SELECT * FROM tmp')
    db.drop('tmp')


config_type = 'website_content'
config_name = 'example'
config = read_config(config_type, config_name)
ingredients = config.get('match').get('ingredients')

db = Database()
data = get_data(db)
matches = get_matches(data, ingredients)
formatted = format_data(matches, ingredients)
save_data(formatted, db)
db.close()
