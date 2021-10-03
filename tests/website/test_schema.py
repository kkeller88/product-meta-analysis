
import pytest

from product_meta_analysis.collect.schema import *

# fixtures for general schema extraction
@pytest.fixture
def schema_list_of_lists():
    ll = [[
        {
            '@context': 'http://schema.org',
            '@type': 'Recipe',
            'recipeIngredient': [
                'ingredient_1',
                'ingredient_2',
                'ingredient_3',
                ]
            },
        {
            '@context': 'http://schema.org',
            '@type': 'Other',
            'Other': [
                'Other',
                'Other',
                'Other',
                ]
            }]]
    return ll

@pytest.fixture
def schema_list():
    l = [{
        '@context': 'http://schema.org',
        '@type': 'Recipe',
        'recipeIngredient': [
            'ingredient_1',
            'ingredient_2',
            'ingredient_3',
            ]
        }]
    return l

@pytest.fixture
def schema_graph():
    g = [{
        '@context': 'http://schema.org',
         '@graph':
            [
            {'@type': 'Recipe',
                'recipeIngredient': [
                    'ingredient_1',
                    'ingredient_2',
                    'ingredient_3',
                    ]
                    },
            {'@type': 'Other_graph_entry',
                'Other': [
                    'other',
                    'other',
                    'other',
                    ]
                },
            ]
        }]
    return g

# fixtures for parsing specific components out of schema
@pytest.fixture
def instructions_schema_list():
    l = {
        '@context': 'http://schema.org',
        '@type': 'Recipe',
        'recipeIngredient': [
            'ingredient_1',
            'ingredient_2',
            'ingredient_3',
            ],
        'recipeInstructions': [
            {'@type':'HowToStep','text':'Step 1'},
            {'@type':'HowToStep','text':'Step 2'},
            ],
        'aggregateRating': {
            '@type':'AggregateRating',
            'ratingValue':1.0,
            'reviewCount':100
            }
        }
    return l

@pytest.fixture
def instructions_schema_list_of_lists():
    l = {
        '@context': 'http://schema.org',
        '@type': 'Recipe',
        'recipeIngredient': [
            'ingredient_1',
            'ingredient_2',
            'ingredient_3',
            ],
        'recipeInstructions': [[
            {'@type':'HowToStep','text':'Step 1'},
            {'@type':'HowToStep','text':'Step 2'},
            ]],
        'aggregateRating': {
            '@type':'AggregateRating',
            'ratingValue':1.0,
            'reviewCount':100
            }
        }
    return l

@pytest.fixture
def instructions_schema_string():
    l = {
        '@context': 'http://schema.org',
        '@type': 'Recipe',
        'recipeIngredient': [
            'ingredient_1',
            'ingredient_2',
            'ingredient_3',
            ],
        'recipeInstructions': 'Step 1;;; Step 2;;; Step 3',
        'aggregateRating': {
            '@type':'AggregateRating',
            'ratingValue':1.0,
            'reviewCount':100
            }
        }
    return l

@pytest.fixture
def recipe_schema_list():
    l = {
        '@context': 'http://schema.org',
        '@type': 'Recipe',
        'recipeIngredient': [
            'ingredient_1',
            'ingredient_2',
            'ingredient_3',
            ],
        'recipeInstructions': 'Step 1;;; Step 2;;; Step 3',
        'aggregateRating': [{
            '@type':'AggregateRating',
            'ratingValue':1.0,
            'reviewCount':100
            }]
        }
    return l

def test_unpack_graph(schema_graph):
    unpacked = unpack_schema_graph(schema_graph)
    assert unpacked[0].get('@type') == 'Recipe'

def test_unpack_list_of_list(schema_list_of_lists):
    unpacked = unpack_list_of_lists(schema_list_of_lists)
    assert unpacked[0].get('@type') == 'Recipe'

def test_unpack_recipe_schema(schema_graph):
    unpacked = unpack_recipe_schema(schema_graph)
    assert len(unpacked) == 1

def test_extract_instructions_list(instructions_schema_list):
    instructions = extract_recipe_instructions(instructions_schema_list)
    assert instructions[0] == 'Step 1'

def test_extract_instructions_list_of_lists(instructions_schema_list_of_lists):
    instructions = extract_recipe_instructions(instructions_schema_list_of_lists)
    assert instructions[0] == 'Step 1'

def test_extract_instructions_string(instructions_schema_string):
    instructions = extract_recipe_instructions(instructions_schema_string)
    assert instructions[0] == 'Step 1;;; Step 2;;; Step 3'

def test_extract_ratings(instructions_schema_list):
    ratings = extract_recipe_ratings(instructions_schema_list)
    assert ratings.get('rating') == 1.0
    assert ratings.get('rating_count') == 100

def test_extract_ratings(recipe_schema_list):
    ratings = extract_recipe_ratings(recipe_schema_list)
    assert ratings.get('rating') == 1.0
    assert ratings.get('rating_count') == 100

def test_extract_ratings(instructions_schema_list):
    ingredients = extract_recipe_ingredients(instructions_schema_list)
    assert ingredients[0].get('full_text') == 'ingredient_1'
