from product_meta_analysis.database import Database
from product_meta_analysis.analyze import tokenize

db = Database()
query = f"""
    select body
    from reddit_comments
    where category = 'gluten_free_flour'
    limit 20
    """
comments = db.read(query)

def get_noun_phrases(comments):
    s = tokenize.Tokenizer()
    comments = [
        s.split_and_extract_tokens(x[0])
        for x in comments
        ]
    return comments

print(get_noun_phrases(comments))
