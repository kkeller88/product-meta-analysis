import pandas as pd


def one_hot_encode_ingredients(recipe, ingredients):
    """Treat each ingredient in a recipe as one observation"""
    encoded_ingredients = [
        {
            ingredient: 1 if ingredient in recipe.get('full_text').lower() else 0
            for ingredient in ingredients
            }
        for recipe in recipe.get('ingredients')
        ]
    encoded_ingredients = pd.DataFrame(encoded_ingredients, columns=ingredients)
    return encoded_ingredients

# TODO: improve legibility
def one_hot_encode_recipes(recipes, ingredients):
    """Treat each recipe as one observation"""
    def combine_all_ingredients(recipe):
        combined = ' ; '.join([
            x.get('full_text')
            for x in recipe.get('ingredients')
            ]).lower()
        return combined

    encoded_recipes = [
        {ingredient: 1 if ingredient in combine_all_ingredients(recipe) else 0
            for ingredient in ingredients
            }
        for recipe in recipes
        ]
    encoded_recipes = pd.DataFrame(encoded_recipes, columns=ingredients)
    return encoded_recipes
