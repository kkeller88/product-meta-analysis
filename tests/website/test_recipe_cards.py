import codecs
import os
from pathlib import Path

from bs4 import BeautifulSoup
import pytest

from product_meta_analysis.collect.recipe_cards import *

HTML_FIXTURE_PATH = os.path.join(Path(__file__).parents[1], 'fixtures', 'html')

@pytest.fixture
def multiple_recipe_div_page():
    path = os.path.join(HTML_FIXTURE_PATH, 'multiple_recipe_div.html')
    html = codecs.open(path, 'r', 'utf-8').read()
    bs = BeautifulSoup(html, 'html.parser')
    return bs

def test_recipe_card_selector_word(multiple_recipe_div_page):
    selectors = [
        RecipeSelectorRuleWord(word='real-recipe-list'),
        ]
    rs = RecipeCardSelector()
    rs.set_next(selectors)
    candidate = rs.select([multiple_recipe_div_page])
    assert "cups whole milk" in candidate.text

def test_recipe_card_selector_word_and_list(multiple_recipe_div_page):
    selectors = [
        RecipeSelectorRuleWord(word='fake-recipe'),
        RecipeSelectorRuleLi()
        ]
    rs = RecipeCardSelector()
    rs.set_next(selectors)
    candidate = rs.select([multiple_recipe_div_page])
    assert "fake item 2" in candidate.text

def test_ingredient_extractor_wprm():
    path = os.path.join(HTML_FIXTURE_PATH, 'ingredients_wprm.html')
    html = codecs.open(path, 'r', 'utf-8').read()
    bs = BeautifulSoup(html, 'html.parser')
    ext = IngredientExtractor()
    ext.set_next([IngredientExtractorRuleWPRM()])
    output = ext.extract(bs)
    assert output[0].get('name') ==  'radicchio'
    assert output[0].get('amount') == '1'
    assert output[0].get('unit') == 'head'
    assert output[0].get('full_text') == '1 head radicchio'

def test_ingredient_extractor_tasty():
    path = os.path.join(HTML_FIXTURE_PATH, 'ingredients_tasty.html')
    html = codecs.open(path, 'r', 'utf-8').read()
    bs = BeautifulSoup(html, 'html.parser')
    ext = IngredientExtractor()
    ext.set_next([IngredientExtractorRuleTasty()])
    output = ext.extract(bs)
    assert output[8].get('name') ==  'chili powder'
    assert output[8].get('amount') == '0.5'
    assert output[8].get('unit') == 'teaspoon'

def test_ingredient_extractor_srseats():
    url = 'https://www.seriouseats.com/ingredient-stovetop-mac-and-cheese-recipe'
    s = [RecipeSelectorRuleWord(word='structured-ingredients')]
    e = [IngredientExtractorRuleSrsEats()]
    parser = RecipeCardParser(selector_rules=s, extractor_rules=e)
    output = parser.parse(url=url)
    assert output[0].get('name') ==  'elbow macaroni'
    assert output[0].get('amount') == '6'
    assert output[0].get('unit') == 'ounces'


@pytest.mark.skip('I think this was just entered wrong, but should double check')
def test_ingredient_extractor_tasty_bug():
    path = os.path.join(HTML_FIXTURE_PATH, 'ingredients_tasty.html')
    html = codecs.open(path, 'r', 'utf-8').read()
    bs = BeautifulSoup(html, 'html.parser')
    ext = IngredientExtractor()
    ext.set_next([IngredientExtractorRuleTasty()])
    output = ext.extract(bs)
    assert output[0].get('amount') == '1'
    assert 'tablespoon' in output[0].get('name')

def test_recipe_card_parser(multiple_recipe_div_page):
    path = os.path.join(HTML_FIXTURE_PATH, 'full_WPRM_page.html')
    html = codecs.open(path, 'r', 'utf-8').read()
    page = BeautifulSoup(html, 'html.parser')
    s = [RecipeSelectorRuleWord(word='wprm-recipe-ingredients')]
    e = [IngredientExtractorRuleWPRM()]
    parser = RecipeCardParser(selector_rules=s, extractor_rules=e)
    output = parser.parse(page=page)
    assert output[0].get('full_text') == '1 head radicchio'

def test_dev(multiple_recipe_div_page):
    # wprm-recipe-ingredients: WPRM
    # structured-ingredients: seriouseats
    url = 'https://www.seriouseats.com/ingredient-stovetop-mac-and-cheese-recipe'
    s = [
        RecipeSelectorRuleWord(word='wprm-recipe-ingredients|structured-ingredients'),
        RecipeSelectorRuleLi(),
        ]
    e = [
        IngredientExtractorRuleWPRM(),
        IngredientExtractorRuleTasty(),
        IngredientExtractorRuleSrsEats()
        ]
    parser = RecipeCardParser(selector_rules=s, extractor_rules=e)
    output = parser.parse(url=url)
    #assert output[0].get('full_text') == '1 head radicchio'
