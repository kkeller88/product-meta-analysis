import spacy


class Tokenizer:
    def __init__(self, model_name="en_core_web_sm"):
        self._model_name = model_name
        self._model = spacy.load(model_name)

    def split_and_extract_tokens(self, text):
        doc = self._model(text)
        return [[y for y in x.noun_chunks] for x in doc.sents]

    def split_sentences(self, text):
        doc = self._model(text)
        return [x for x in doc.sents]

    def split_and_extract_entities(self, text):
        doc = self._model(text)
        return [[y for y in x.ents] for x in doc.sents]
