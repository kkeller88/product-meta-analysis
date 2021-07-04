import pytest

@pytest.fixture
def body_text():
    text = "I personally prefer the Bob's Red Mill flour " \
        "to the King Arthur flour. It is a much better substitute" \
        "for regular all purpose flour."
    return text
