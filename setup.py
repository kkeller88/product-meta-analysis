import setuptools

REQUIRES = [
    "spacy",
    "sqlite",
    "pyyaml",
    "praw"
    ]
EXTRA_REQUIRES = {
    'dev' : [
        'pytest'
    ]
}
setuptools.setup()
