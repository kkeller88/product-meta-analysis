from product_meta_analysis.database.database import Database


# TODO: condense/parameterize this; lots of duplicated code; should
#   probably run this off of yaml config files in the long run
# TODO: migrate to brand_id hash rather than brand_ix for reddit comments
# TODO: save base thread id in a third reddit table
def create_comment_annotation_table(db):
    table_name = "reddit_comment_annotations"
    try:
        db.drop(table_name)
    except:
        pass
    query = f""" CREATE TABLE IF NOT EXISTS {table_name} (
        comment_id text,
        sentence_ix int,
        brand text,
    	sentiment text,
        brand_ix int,
        annotation_id text PRIMARY KEY,
        process_datetime timestamp,
        process_date date,
        UNIQUE(annotation_id)
        )"""
    db.write(query)

def create_comment_table(db):
    table_name = "reddit_comments"
    try:
        db.drop(table_name)
    except:
        pass
    query = f""" CREATE TABLE IF NOT EXISTS {table_name} (
        comment_id text PRIMARY KEY,
        body text,
        upvotes int,
        parent_id text,
        subreddit text,
        category text,
        process_datetime timestamp,
        process_date date,
        UNIQUE(comment_id)
        )"""
    db.write(query)

def create_website_url_table(db):
    table_name = "website_urls"
    try:
        db.drop(table_name)
    except:
        pass
    query = f""" CREATE TABLE IF NOT EXISTS {table_name} (
        url_id text PRIMARY KEY,
        url text,
        domain text,
        process_datetime timestamp,
        process_date date,
        UNIQUE(url_id)
        )"""
    db.write(query)

def create_website_content_table(db):
    table_name = "website_content"
    try:
        db.drop(table_name)
    except:
        pass
    query = f""" CREATE TABLE IF NOT EXISTS {table_name} (
        url_id text PRIMARY KEY,
        url text,
        body text,
        process_datetime timestamp,
        process_date date,
        UNIQUE(url_id)
        )"""
    db.write(query)

def create_website_annotation_table(db):
    table_name = "website_content_annotations"
    try:
        db.drop(table_name)
    except:
        pass
    query = f""" CREATE TABLE IF NOT EXISTS {table_name} (
        url_id text PRIMARY KEY,
        sentence_ix int,
        brand text,
        brand_id int,
    	sentiment text,
        annotation_id text PRIMARY KEY,
        process_datetime timestamp,
        process_date date,
        UNIQUE(annotation_id)
        )"""
