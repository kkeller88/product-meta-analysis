
import pytest

from product_meta_analysis.collect.schema import *

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

def test_unpack_graph(schema_graph):
    unpacked = unpack_schema_graph(schema_graph)
    assert unpacked[0].get('@type') == 'Recipe'

def test_unpack_list_of_list(schema_list_of_lists):
    unpacked = unpack_list_of_lists(schema_list_of_lists)
    assert unpacked[0].get('@type') == 'Recipe'

def test_unpack_recipe_schema(schema_graph):
    unpacked = unpack_recipe_schema(schema_graph)
    assert len(unpacked) == 1
