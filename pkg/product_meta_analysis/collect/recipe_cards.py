import re
import requests

from bs4 import BeautifulSoup


class IngredientExtractor:
    def __init__(self):
        pass

    def get_ingredients(self, url):
        rqst = requests.get(url).text
        soup = BeautifulSoup(rqst, 'html.parser')
        try:
            ingredients = self._get_ingredient_div(soup)
            extract = self._extract_ingredients(ingredients)
            return extract
        except Exception as e:
            print(f'Skipped URL {url} because {e}')

    def _get_ingredient_div(self, soup):
        ingredients = soup.findAll('div', class_=re.compile('ingredients'))
        if len(ingredients) == 1:
            return ingredients[0]
        else:
            raise Exception(f'Multiple ingredients divs found!')

    def _extract_ingredients(self, ingredients):
        if 'wprm-recipe' in ' '.join(ingredients["class"]):
            extract = self._extract_ingredients_wprm(ingredients)
        elif 'tasty-recipe' in ' '.join(ingredients["class"]):
            extract = self._extract_ingredients_tasty(ingredients)
        else:
            raise Exception ('Recipe card format not recognized!')
        return extract

    def _extract_ingredients_wprm(self, ingredients):
        def get_span_item(span, item_name):
            item = x.find("span", class_=item_name)
            return item.text if item is not None else None

        extract = []
        for x in ingredients.findAll('li'):
            name = get_span_item(x, "wprm-recipe-ingredient-name")
            amount = get_span_item(x, "wprm-recipe-ingredient-amount")
            unit = get_span_item(x, "wprm-recipe-ingredient-unit")
            extract.append({'name': name, 'amount':amount, 'unit': unit})
        return extract

    def _extract_ingredients_tasty(self, ingredients):
        extract = []
        for x in ingredients.findAll('li'):
            name = x.contents[-1]
            amount = x["data-amount"] if x.get("data-amount", None) is not None else None
            unit = x["data-unit"] if x.get("data-unit", None) is not None else None
            extract.append({'name': name, 'amount':amount, 'unit': unit})
        return extract
