import datetime

import pandas as pd

from product_meta_analysis.database.database import Database
from product_meta_analysis.collect.reddit import Reddit
from product_meta_analysis.utils import read_config


def get_comments(post_ids, category):
	r = Reddit(rest=1)
	c = [
		r.get_all_comments_formatted(id, category=category)
		for id in post_ids
		]
	comments = pd.concat(c)
	comments['process_datetime'] = datetime.datetime.now()
	comments['process_date'] = datetime.date.today()
	return comments

def save_comments(data, database):
	data.to_sql(
		name='tmp',
		con=database._con,
		if_exists = 'append',
		index=False
		)
	db.write('INSERT OR IGNORE INTO reddit_comments SELECT * FROM tmp')
	db.drop('tmp')


file_name = 'gluten_free_flour'
config_name = 'reddit_comments'
db = Database()
post_ids = read_config(config_name, file_name).get('post_ids')
comments = get_comments(post_ids, category=file_name)
save_comments(comments, db)
db.close()
