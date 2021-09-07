import datetime
import json

import pandas as pd

from product_meta_analysis.database.database import Database
from product_meta_analysis.utils import read_config
from product_meta_analysis.collect.recipe_cards import IngredientExtractor


CONTENT_TYPE = 'recipe_card_ingredients'


extractor = IngredientExtractor()

def to_sql_domains(domains):
	return '"' + '" or domain is "'.join(domains) + '"'

def get_urls(db, domains):
	query = f"""
		select url_id, url
		from website_urls
		where (domain is {to_sql_domains(domains)})
		"""
	urls = db.read(query)
	return urls

def get_matches(urls, match_terms):
	matches = [
		(id, url)
		for id, url in urls
		for match_term in match_terms
		if match_term in url
		]
	return matches

def get_content_(urls):
	content = [
		[url[0], url[1], json.dumps(extractor.get_ingredients(url[1]))]
		for url in urls
		]
	content = pd.DataFrame(content, columns=['url_id', 'url', 'content'])
	content['content_type'] = CONTENT_TYPE
	content['process_datetime'] = datetime.datetime.now()
	content['process_date'] = datetime.date.today()
	return content

def save_content(data, db):
    data.to_sql(
        name='tmp',
        con=db._con,
        if_exists = 'append',
        index=False
        )
    db.write('INSERT OR IGNORE INTO website_content SELECT * FROM tmp')
    db.drop('tmp')



config_type = 'website_content'
config_name = 'example'
config = read_config(config_type, config_name)
domains = config.get('urls').get('domains')
match_terms = config.get('content').get('match_terms')

db = Database()
urls = get_urls(db, domains)
matches = get_matches(urls, match_terms)
content = get_content_(matches)
save_content(content, db)
