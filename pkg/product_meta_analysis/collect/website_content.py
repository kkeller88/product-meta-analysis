import re
import requests

from bs4 import BeautifulSoup


def get_content(urls):
    return ['id', 'url', 'This is a test']

class IngredientExtractor:
    def __init__(self):
        pass

    def get_ingredients(self, url):
        rqst = requests.get(url).text
        soup = BeautifulSoup(rqst, 'html.parser')
        ingredients = self._get_ingredient_div(soup)
        extract = self._extract_ingredients(ingredients)

    def _get_ingredient_div(self, soup):
        ingredients = soup.findAll('div', class_=re.compile('ingredients'))
        if len(ingredients) == 1:
            return ingredients[0]
        else:
            raise Exception('Multiple ingredients divs found!')

    def _extract_ingredients(self, ingredients):
        if 'wprm-recipe' in ' '.join(ingredients["class"]):
            extract = self._extract_ingredients_wprm(ingredients)
        else:
            raise Exception ('Recipe card format not recognized!')

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

url = "https://cookieandkate.com/spicy-squash-soup-recipe/"
url = "https://aglutenfreeplate.com/gluten-free-pretzel-bites/"

IngredientExtractor().get_ingredients(url)
