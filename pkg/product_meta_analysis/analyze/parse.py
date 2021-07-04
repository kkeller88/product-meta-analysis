import spacy


class Sentencizer:
    def __init__(self, model_name="en_core_web_sm"):
        self._model_name = model_name
        self._model = spacy.load(model_name)

    def split(self, text):
        doc = self._model(text)
        return [x for x in doc.sents]
