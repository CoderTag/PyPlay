from pytest_bdd import scenario

@scenario('../features/google_search.feature', 'Search for a keyword on Google')
def test_google_search():
    pass