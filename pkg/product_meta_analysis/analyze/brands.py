import operator

from nltk import ngrams

class BrandRecognizerBase:
    def __init__(self, brands):
        self.brands = brands

    def get_brands(self, sentences):
        brands = [
            strip_nulls([self._get_brand(token) for token in sentence])
            for sentence in sentences
            ]
        return brands

class FuzzyBrandRecognizer(BrandRecognizerBase):
    def __init__(self, brands):
        super().__init__(brands=brands)
        self.n_grams = 3
        self.brands_ngrams = {x:self._get_ngram_strings(x, self.n_grams) for x in self.brands}
        self.min_token_length = 5
        self.jaccard_threshold = 0.25

    def _get_brand(self, token:str):
        n_char = token.end_char - token.start_char
        if n_char >= self.min_token_length:
            token_ngrams = self._get_ngram_strings(token.text, self.n_grams)
            scores = {
                k:self._get_jaccard_dist(token_ngrams, v)
                for k, v in self.brands_ngrams.items()
                }
            best_match, best_score = max(
                scores.items(),
                key=operator.itemgetter(1)
                )
            if best_score > self.jaccard_threshold:
                return best_match

    @staticmethod
    def _get_ngram_strings(s, n):
        return [''.join(x).lower() for x in ngrams(s, n)]

    @staticmethod
    def _get_jaccard_dist(list1, list2):
        s1 = set(list1)
        s2 = set(list2)
        return float(len(s1.intersection(s2))) / float(len(s1.union(s2)))

def strip_nulls(l):
    return [x for x in set(l) if x is not None]
