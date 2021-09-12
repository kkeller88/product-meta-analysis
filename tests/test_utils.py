from product_meta_analysis.utils import condition_to_sql


def test_get_urls():
    expected = 'domain is "a" or domain is "b" or domain is "c"'
    assert condition_to_sql(['a', 'b', 'c']) == expected

def test_get_urls_on():
    expected = 'z is "a" or z is "b" or z is "c"'
    assert condition_to_sql(['a', 'b', 'c'], 'z') == expected

def test_get_urls_like():
    expected = 'domain like "%a%" or domain like "%b%" or domain like "%c%"'
    assert condition_to_sql(['a', 'b', 'c'], allow_like=True) == expected

def test_get_urls_none():
    assert condition_to_sql([]) == "False"

def test_get_urls_empty():
    assert condition_to_sql(None) == "False"
