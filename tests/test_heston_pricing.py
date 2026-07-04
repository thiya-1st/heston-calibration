from src.heston_pricing import heston_call_price
from src.parameters import HestonParameters
import pytest

@pytest.fixture
def price():
    return heston_call_price(100, 100, 1, 0.05, DEFAULT_PARAMS)

DEFAULT_PARAMS = HestonParameters(
    v0 = 0.04,
    theta = 0.04,
    kappa = 2,
    xi = 0.3,
    rho = -0.7,
)

def test_heston_price_is_positive(price):
    assert price > 0

def test_heston_price_is_less_than_stock_price(price):
    assert price < 100

def test_heston_price_is_float(price):
    assert isinstance(price, float)

def test_higher_stock_price_increases_heston_price():
    low_price = heston_call_price(90, 100, 1, 0.05, DEFAULT_PARAMS)
    high_price = heston_call_price(110, 100, 1, 0.05, DEFAULT_PARAMS)
    assert high_price > low_price

def test_higher_strike_decreases_heston_price():
    high_price = heston_call_price(100, 90, 1, 0.05, DEFAULT_PARAMS)
    low_price = heston_call_price(100, 110, 1, 0.05, DEFAULT_PARAMS)
    assert high_price > low_price
