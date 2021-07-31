from product_meta_analysis.database.database import Database


# TODO: condense/parameterize this; lots of duplicated code
def create_comment_annotation_table(db):
    table_name = "reddit_comment_annotations"
    try:
        db.drop(table_name)
    except:
        pass
    query = f""" CREATE TABLE IF NOT EXISTS {table_name} (
        id text,
        sentence_ix int,
        brands text,
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
        id text PRIMARY KEY,
        body text,
        upvotes int,
        parent_id text,
        subreddit text,
        category text,
        process_datetime timestamp,
        process_date date,
        UNIQUE(id)
        )"""
    db.write(query)
