import pytest
from bsdapi.Filters import Filters
from bsdapi.Filters import FilterError


def test_get_query_failure():
    """
    Filters does not produce a query if any of the keys are not known
    """
    vals = {"this_key_does_not_exist": 123}
    filters = Filters(vals)

    with pytest.raises(FilterError):
        filters.getQuery()


@pytest.mark.parametrize("state_cd", ["AZ", ["AZ"]])
def test_get_query_single_state(state_cd):
    """
    A single state_cd should be added to the query as-is
    """
    vals = {"state_cd": state_cd}
    filters = Filters(vals)
    query = filters.getQuery()
    assert query["state_cd"] == "AZ"


def test_get_query_multi_state():
    """
    Multiple states should be added to the query as a comma-separated list, enclosed by parentheses
    """
    vals = {"state_cd": ["AZ", "WY"]}
    filters = Filters(vals)
    query = filters.getQuery()
    assert query["state_cd"] == "(AZ,WY)"


@pytest.mark.parametrize("key", ["is_subscribed", "has_account"])
def test_get_query_subscribed(key):
    """
    Subscription status is included when it is in the affirmative
    """
    vals = {key: True}
    filters = Filters(vals)
    query = filters.getQuery()
    assert query[key] is True


@pytest.mark.parametrize("key", ["is_subscribed", "has_account"])
def test_get_query_not_subscribed(key):
    """
    Unsubscribed is treated the same way as unknown: it is omitted from the query
    """
    vals = {key: False}
    filters = Filters(vals)
    query = filters.getQuery()
    assert key not in query


@pytest.mark.parametrize("key", ["primary_state_cd", "signup_form_id", "email"])
def test_get_query_remaining(key):
    """
    Some fields are simply copied to the query as-is
    """
    vals = {key: "some-value"}
    filters = Filters(vals)
    query = filters.getQuery()
    assert query[key] == "some-value"
