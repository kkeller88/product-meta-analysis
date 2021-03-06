import datetime
import json

import pandas as pd

from product_meta_analysis.database.database import Database
from product_meta_analysis.utils import read_config, condition_to_sql
from product_meta_analysis.collect.recipe_cards import *



def get_urls(db, domains, manual_urls, match_terms):
	query = f"""
		select url_id, url
		from website_urls
		where (({condition_to_sql(domains)}) and ({condition_to_sql(match_terms, on="url", allow_like=True)}))
			or ({condition_to_sql(manual_urls, on="url")})
		"""
	urls = db.read(query)
	return urls

def get_content_(urls, content_type):
	def build_recipe_card_parser():
		s = [RecipeSelectorRuleSchema()]
		e = [IngredientExtractorRuleSchema()]
		parser = RecipeCardParser(selector_rules=s, extractor_rules=e)
		return parser

	def extract_url_content(url, parser):
		content = json.dumps(parser.parse(url))
		return content

	parser = build_recipe_card_parser()
	content = [
		[url[0], url[1], extract_url_content(url[1], parser)]
		for url in urls
		]
	content = pd.DataFrame(content, columns=['url_id', 'url', 'content'])
	content['content_type'] = content_type
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
manual_urls = config.get('urls').get('urls')
match_terms = config.get('content').get('match_terms')
content_type = config.get('content').get('content_type')

db = Database()
matches = get_urls(db, domains, manual_urls, match_terms)
content = get_content_(matches, content_type)
save_content(content, db)
