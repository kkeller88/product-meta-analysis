from abc import abstractmethod
import itertools
import re
import requests

from bs4 import BeautifulSoup
from bs4.element import NavigableString


class RecipeCardParser:
    def __init__(self, selector_rules, extractor_rules):
        self.sel = RecipeCardSelector()
        self.ext = IngredientExtractor()
        self.sel.set_next(selector_rules)
        self.ext.set_next(extractor_rules)

    def get_page(self, url):
        rqst = requests.get(url).text
        soup = BeautifulSoup(rqst, 'html.parser')
        return soup

    def parse(self, url=None, page=None):
        if not page:
            page = self.get_page(url)
        recipe_card = self.sel.select([page])
        ingredients = self.ext.extract(recipe_card)
        return ingredients

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


class IngredientExtractor:
    def __init__(self):
        self._extractors = []

    def set_next(self, next_extractor):
        self._extractors.extend(next_extractor)

    def extract(self, recipe):
        for extractor in self._extractors:
            is_correct_format = extractor.check_correct_format(recipe)
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
        class_ = recipe.find('div')["class"][0]
        return True if 'wprm' in class_ else False

    def extract_data(self, recipe):
        extract = []
        for x in recipe.findAll('li'):
            name = get_span_item(x, "wprm-recipe-ingredient-name")
            amount = get_span_item(x, "wprm-recipe-ingredient-amount")
            unit = get_span_item(x, "wprm-recipe-ingredient-unit")
            full_text = x.text
            extract.append({
                'name': name,
                'amount':amount,
                'unit': unit,
                'full_text':full_text
                })
        return extract

class IngredientExtractorRuleTasty:
    def check_correct_format(self, recipe):
        class_ = recipe.find('div')["class"][0]
        return True if 'tasty-recipe' in class_ else False

    # NOTE: assumes you only have a unit if you have an amount
    def extract_data(self, recipe):
        extract = []
        for x in recipe.findAll('li'):
            amount_span = x.find("span", {'data-amount':True})
            if amount_span:
                name = "".join([
                        t if type(t)==NavigableString
                        else '#'
                        for t in x.find("span").contents
                        ]) \
                    .strip() \
                    .strip('#') \
                    .strip()
                amount = amount_span.get('data-amount')
                unit = amount_span.get('data-unit', None)
            else:
                name = x.text
                amount = None
                unit = None
            full_text = x.text
            extract.append({
                'name': name,
                'amount':amount,
                'unit': unit,
                'full_text': full_text
                })
        return extract

def get_span_item(span, item_name):
    item = span.find("span", class_=item_name)
    return item.text if item is not None else None
