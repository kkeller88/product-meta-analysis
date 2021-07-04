
from product_meta_analysis.database import Database


db = Database()

# create table
create_query = f""" CREATE TABLE IF NOT EXISTS urls (
	url text PRIMARY KEY,
	site text NOT NULL,
    UNIQUE(url)
    )"""
db.write(create_query)


print(db.read("select * from urls limit 50"))
