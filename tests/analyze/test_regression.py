import pytest

from product_meta_analysis.analyze.regression import *

@pytest.fixture()
def recipe():
    recipe = {
        'ingredients': [
            {
                'name': None,
                'amount': None,
                'unit': None,
                'full_text': 'gouda cheese'
                },
            {
                'name': None,
                'amount': None,
                'unit': None,
                'full_text': 'cheddar cheese'
                },
            ],
        'rating': {
            'rating': 4.0,
            'rating_count': 100
            },
        'instructions': [
            'Step 1',
            'Step 2',
            'Step 11',
            ]
        }
    return recipe

@pytest.fixture()
def ingredients():
    return ['gouda', 'cheddar']

def test_one_hot_encode_ingredients(recipe, ingredients):
    data = one_hot_encode_ingredients(recipe, ingredients)
    assert data['gouda'].iloc[0] == 1
    assert data['cheddar'].iloc[0] == 0

def test_one_hot_encode_recipes(recipe, ingredients):
    recipes = [recipe, recipe]
    data = one_hot_encode_recipes(recipes, ingredients)
    assert data['gouda'].iloc[0] == 1
    assert data['gouda'].iloc[1] == 1
    assert data.shape[0] == 2
