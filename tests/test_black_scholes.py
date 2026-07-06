import numpy as np
from src.black_scholes import black_scholes_call
import pytest

def test_black_scholes_scalar():
    assert black_scholes_call(100, 110, 1, 0.05, 0.2) == pytest.approx(6.040088129724239)
    
def test_black_scholes_array():
    S = np.array([90, 100, 110])
    result = black_scholes_call(S, 110, 1, 0.05, 0.2)
    expected = np.array([2.52371566, 6.04008813, 11.49564193])
    np.testing.assert_allclose(result, expected)

def test_higher_volatility_increases_call_price():
    price_low_vol = black_scholes_call(100, 110, 1, 0.05, 0.1)
    price_high_vol = black_scholes_call(100, 110, 1, 0.05, 0.3)
    assert price_high_vol > price_low_vol

def test_higher_strike_decreases_call_price():
    price_low_strike = black_scholes_call(100, 110, 1, 0.05, 0.2)
    price_high_strike = black_scholes_call(100, 130, 1, 0.05, 0.2)
    assert price_high_strike < price_low_strike

def test_higher_stock_price_increases_call_price():
    price_low_stock_price = black_scholes_call(100, 110, 1, 0.05, 0.2)
    price_high_stock_price = black_scholes_call(120, 110, 1, 0.05, 0.2)
    assert price_high_stock_price > price_low_stock_price
