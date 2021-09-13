from abc import abstractmethod
import itertools
import re
import requests

from bs4 import BeautifulSoup


class RecipeCardSelector:
    def __init__(self):
        self._selectors = []

    def set_next(self, next_selector):
        self._selectors.extend(next_selector)

    def select(self, candidates):
        for selector in self._selectors:
            candidates = selector.make_selection(candidates)
            if len(candidates) == 1:
                return candidates[0]
        if len(candidates) == 0:
            raise Exception('No valid candidates found!')
        else:
            raise Exception('Could not narrow down to a single candidate')

class RecipeSelectorRuleBase:
    def __init__(self, return_filtered=True):
        self.return_filtered = return_filtered

    @abstractmethod
    def make_selection(self, candidates):
        return candidates

class RecipeSelectorRuleWord(RecipeSelectorRuleBase):
    def __init__(self, word = 'ingredients', type='div', return_filtered=True):
        self.word = word
        self.type = type
        self.return_filtered = return_filtered

    def make_selection(self, candidates):
        candidates = [
            x.findAll(self.type, class_=re.compile(self.word))
            for x in candidates
            ]
        candidates = list(itertools.chain.from_iterable(candidates))
        return candidates

class RecipeSelectorRuleLi(RecipeSelectorRuleBase):
    def make_selection(self, candidates):
        candidates = [
            x
            for x in candidates
            if x.findAll('li')
            ]
        return candidates


class IngredientExtractorEngine:
    def __init__(self):
        self._extractors = []

    def set_next(self, next_extractor):
        self._extractors.extend(next_extractor)

    def extract(self, recipe):
        for extractor in self._extractors:
            is_correct_format = extractor.check_correct_format(recipe)
            print(is_correct_format)
            if is_correct_format:
                ingredients = extractor.extract_data(recipe)
                return ingredients

class IngredientExtractorRuleBase:
    def __init__(self):
        pass

    @abstractmethod
    def check_correct_format(self, recipe):
        return False

    @abstractmethod
    def extract_data(self, recipe):
        return recipe

class IngredientExtractorRuleWPRM:
    def check_correct_format(self, recipe):
        li_class = recipe.find('li')["class"][0]
        return True if 'wprm-recipe' in li_class else False

    def extract_data(self, recipe):
        extract = []
        for x in recipe.findAll('li'):
            name = get_span_item(x, "wprm-recipe-ingredient-name")
            amount = get_span_item(x, "wprm-recipe-ingredient-amount")
            unit = get_span_item(x, "wprm-recipe-ingredient-unit")
            extract.append({'name': name, 'amount':amount, 'unit': unit})
        return extract


# TODO: A lot of this needs to be generalized
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
        selectors = [
            RecipeSelectorRuleWord(word='fake-recipe'),
            RecipeSelectorRuleLi()
            ]
        rs = RecipeCardSelector()
        rs.set_next(selectors)
        candidate = rs.select([soup])
        return candidate

    def _extract_ingredients(self, recipe):
        extractors = [
            IngredientExtractorRuleWPRM()
            ]
        ex = IngredientExtractorEngine()
        ex.set_next(extractors)
        ingredients = ex.extract(recipe)
        return ingredients

    def _extract_ingredients_tasty(self, ingredients):
        extract = []
        for x in ingredients.findAll('li'):
            name = x.contents[-1]
            amount = x["data-amount"] if x.get("data-amount", None) is not None else None
            unit = x["data-unit"] if x.get("data-unit", None) is not None else None
            extract.append({'name': name, 'amount':amount, 'unit': unit})
        return extract

    def _extract_ingredients_general(self, ingredients):
        extract = []
        for x in ingredients.findAll('li'):
            name = get_span_item(x, "wprm-recipe-ingredient-name")
            amount = get_span_item(x, "wprm-recipe-ingredient-amount")
            unit = get_span_item(x, "wprm-recipe-ingredient-unit")
            extract.append({'name': name, 'amount':amount, 'unit': unit})
        return extract

def get_span_item(span, item_name):
    item = span.find("span", class_=item_name)
    return item.text if item is not None else None
