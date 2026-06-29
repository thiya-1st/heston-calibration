from src.black_scholes import black_scholes_call
from src.implied_volatility import implied_volatility
import pytest

def test_known_volatilities():
    true_vols = [0.1, 1.3, 2.4]
    for true_vol in true_vols:
        market_price = black_scholes_call(100, 110, 1, 0.05, true_vol)
        implied_vol = implied_volatility(100, 110, 1, 0.05, market_price)
        assert true_vol == pytest.approx(implied_vol)

def test_boundary_vol():
    boundary_vol = 0.001
    market_price = black_scholes_call(100, 110, 1, 0.05, boundary_vol)
    implied_vol = implied_volatility(100, 110, 1, 0.05, market_price)
    assert boundary_vol == pytest.approx(implied_vol)

def test_invalid_market_price():
    with pytest.raises(ValueError, match = "Root is not bracketed by the initial volatility bounds."):
        implied_volatility(100, 110, 1, 0.05, market_price = -5)

def test_out_of_bounds_vol():
    true_vol = 3.5
    market_price = black_scholes_call(100, 110, 1, 0.05, true_vol)
    with pytest.raises(ValueError, match = "Root is not bracketed by the initial volatility bounds."):
        implied_volatility(100, 110, 1, 0.05, market_price)

def test_iteration_limit():
    true_vol = 0.5
    market_price = black_scholes_call(100, 110, 1, 0.05, true_vol)
    with pytest.raises(RuntimeError, match = "Maximum number of iterations reached."):
        implied_volatility(100, 110, 1, 0.05, market_price, max_iterations = 1)