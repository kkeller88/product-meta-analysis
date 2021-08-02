import os
from pathlib import Path

import pandas as pd
import pytest

from product_meta_analysis.aggregate import reddit as r

FIXTURE_DIR = Path(__file__).parents[1]


@pytest.fixture
def comments_with_annotations():
    cwa_path = os.path.join(FIXTURE_DIR, 'fixtures/comments_with_annotations.csv')
    return pd.read_csv(cwa_path)

def test_get_top_level_comments(comments_with_annotations):
    top_level = r.get_top_level_comments(comments_with_annotations)
    assert top_level.shape[0] <  comments_with_annotations.shape[0]
    assert top_level.shape[0] == 6

def test_append_parent_name_and_type(comments_with_annotations):
    comments = r.append_parent_name_and_type(comments_with_annotations)
    assert 'parent_type' in comments.columns
    assert comments['parent_type'].iloc[0] == 't3'
    assert comments['parent_name'].iloc[0] == 'post1'

def test_append_brand_counts(comments_with_annotations):
    comments = r.append_brand_counts(comments_with_annotations)
    assert 'brand_count' in comments.columns
    assert comments[comments['comment_id'] == 'comment1']['brand_count'].iloc[0] == 3
    assert comments[comments['comment_id'] == 'comment2']['brand_count'].iloc[0] == 2

def test_get_eligible_top_level_comments(comments_with_annotations):
    eligible = r.get_eligible_top_level_comments(comments_with_annotations)
    assert eligible.shape[0] == 2
    assert 'comment1' not in eligible['comment_id']
    assert 'comment3' not in eligible['comment_id']

def test_get_brand_summary(comments_with_annotations):
    brand_summary = r.get_brand_summary(comments_with_annotations)
    king_arthur = brand_summary[brand_summary['Brand']=='King Arthur']
    assert king_arthur['Total Votes'].iloc[0] == 10
    assert king_arthur['Total Comments'].iloc[0] == 4
