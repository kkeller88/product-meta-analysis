import re

# NOTE: t3_threadid are top level comments and t1_commentid are lower level comments
def append_parent_name_and_type(comments):
    comments['parent_name'] = comments['parent_id'].map(lambda x: x[3:])
    comments['parent_type'] = comments['parent_id'].map(lambda x: x[:2])
    return comments

def get_top_level_comments(comments, keep_parent_meta=False):
    if 'parent_type' not in comments.columns:
        comments = append_parent_name_and_type(comments)
    comments = comments[comments['parent_type'] == 't3']
    if not keep_parent_meta:
        comments = comments.drop(['parent_name', 'parent_type'], axis=1)
    return comments

def append_brand_counts(comments):
    """
    Append a column 'brand_count' with the number of unique brands that
    are mentioned in each individual comment.
    """
    brand_counts = comments \
        .groupby('comment_id') \
        .apply(lambda x: len(set(x['brand']))) \
        .reset_index()\
        .rename(columns={0:'brand_count'})
    comments = comments.merge(brand_counts, on='comment_id', how='left')
    return comments

def get_eligible_top_level_comments(comments):
    """
    Get top level comments that mention no more the 2 different brands.
    """
    comments = append_brand_counts(comments)
    top_level = get_top_level_comments(comments, keep_parent_meta=True)
    elligible_comments = top_level[top_level['brand_count'] <= 2] \
        .drop_duplicates(subset=['comment_id', 'brand'])
    return elligible_comments

def get_summary_stats(df):

    return {
        'posts': df['parent_id'].nunique(),
        'comments': df['comment_id'].nunique(),
        'upvotes': df.drop_duplicates('comment_id')['upvotes'].sum(),
        'brands': df['brand'].nunique()
        }

def get_brand_summary(comments):
    agg_ = ['sum', 'count', 'mean']
    brand_summary = comments \
        .groupby(['brand']) \
        .agg({'upvotes': agg_}) \
        .sort_values(('upvotes','sum'), ascending=False) \
        .reset_index() \
        .round(1)
    brand_summary.columns = [
        'Brand',
        'Total Votes',
        'Total Comments',
        'Average Votes per Comment'
        ]
    return brand_summary
