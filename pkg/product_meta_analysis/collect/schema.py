import itertools
from product_meta_analysis.utils import strip_excess_whitespace

# unpack schema
def unpack_list_of_lists(l):
    if isinstance(l[0], list):
        return list(itertools.chain.from_iterable(l))
    else:
        return l

def unpack_schema_graph(l):
    if not isinstance(l[0], dict):
        return l
    else:
        graph_contents = []
        # TODO: CHECK THAT IT IS SCHEMA MARKUP
        for x in l:
            if '@graph' in x.keys():
                graph = x.pop('@graph')
                for entry in graph:
                    entry['@context'] = 'http://schema.org'
                graph_contents.extend(graph)
                graph_contents.append(x)
            else:
                graph_contents.append(x)
        return graph_contents

def check_for_context_schema(x):
    context = x.get('@context')
    if isinstance(context, str) and ("schema.org" in context):
        is_schema = True
    elif isinstance(context, dict) and ("schema.org" in context.get("@vocab")):
        is_schema = True
    else:
        is_schema = False
    return is_schema

def unpack_recipe_schema(s):
    s = unpack_list_of_lists(s)
    s = unpack_schema_graph(s)
    recipe = [
        x
        for x in s
        if check_for_context_schema(x)
            and (x.get('@type') == 'Recipe')]
    return recipe

# parse out specific componentsss
def extract_recipe_instructions(recipe):
    KEYWORD = 'recipeInstructions'
    PLACEHOLDER = []
    instructions = recipe.get(KEYWORD, PLACEHOLDER)
    if isinstance(instructions, str):
        instructions = [{'text': instructions}]
    elif isinstance(instructions, list) and isinstance(instructions[0], list):
        instructions = unpack_list_of_lists(instructions)
    instructions = [
        x.get('text', None)
        for x in instructions
        ]
    return instructions

def extract_recipe_ratings(recipe):
    KEYWORD = 'aggregateRating'
    PLACEHOLDER = {}
    rating = recipe.get(KEYWORD, PLACEHOLDER)
    if isinstance(rating, list):
        rating = rating[0]
    rating = {
        'rating': rating.get('ratingValue', None),
        'rating_count': rating.get('reviewCount', None)
        }
    return rating

def extract_recipe_ingredients(recipe):
    KEYWORD = 'recipeIngredient'
    PLACEHOLDER = []
    ingredients = recipe.get(KEYWORD, PLACEHOLDER)
    ingredients = [
        {
            'name': None,
            'amount': None,
            'unit': None,
            'full_text': strip_excess_whitespace(x)
            }
        for x in ingredients
        ]
    return ingredients
