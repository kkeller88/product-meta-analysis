import codecs
import os
from pathlib import Path

from bs4 import BeautifulSoup

from product_meta_analysis.collect.recipe_cards import IngredientExtractor

HTML_FIXTURE_PATH = os.path.join(Path(__file__).parents[1], 'fixtures', 'html')


def test_ingredient_extractor_wprm():
    path = os.path.join(HTML_FIXTURE_PATH, 'ingredients_wprm.html')
    html = codecs.open(path, 'r', 'utf-8').read()
    ext = IngredientExtractor()
    bs = BeautifulSoup(html, 'html.parser')
    output = ext._extract_ingredients_wprm(bs)
    assert output[0].get('name') ==  'radicchio'
    assert output[0].get('amount') == '1'
    assert output[0].get('unit') == 'head'

def test_ingredient_extractor_tasty():
    pass
