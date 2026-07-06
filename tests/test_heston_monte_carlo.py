from src.heston_pricing import heston_monte_carlo_price
from src.parameters import HestonParameters
from src.black_scholes import black_scholes_call
import numpy as np
import pytest

DEFAULT_PARAMS = HestonParameters(
    v0 = 0.04,
    theta = 0.04,
    kappa = 2,
    xi = 0.3,
    rho = -0.7,
)

@pytest.fixture
def price():
    return heston_monte_carlo_price(100, 100, 1, 0.05, DEFAULT_PARAMS, 100000, 10)

def heston_mc_price_is_positive(price):
    assert price > 0

def test_heston_mc_price_is_less_than_stock_price(price):
    assert price < 100

def test_higher_time_increases_heston_mc_price():
    low_price = heston_monte_carlo_price(100, 100, 1, 0.05, DEFAULT_PARAMS, 100000, 10)
    high_price = heston_monte_carlo_price(100, 100, 2, 0.05, DEFAULT_PARAMS, 100000, 10)
    assert high_price > low_price

def test_higher_strike_decreases_heston_mc_price():
    high_price = heston_monte_carlo_price(100, 90, 1, 0.05, DEFAULT_PARAMS, 100000, 10)
    low_price = heston_monte_carlo_price(100, 110, 1, 0.05, DEFAULT_PARAMS, 100000, 10)
    assert high_price > low_price

def test_heston_mc_price_is_approx_bs_price():
    S, K, T, r = 100, 100, 1, 0.05
    sigma = 0.2
    params = HestonParameters(
        v0 = sigma**2,
        theta = sigma**2,
        kappa = 1,
        xi = 0,
        rho = 0,
    )
    bs_price = black_scholes_call(S, K, T, r, sigma)
    heston_price = heston_monte_carlo_price(100, 100, 1, 0.05, params, 100000, 10)
    assert heston_price == pytest.approx(bs_price, abs = 0.5)

def test_heston_mc_price_convergence():
    S, K, T, r = 100, 100, 1, 0.05
    np.random.seed(42)

    price_10k = heston_monte_carlo_price(S, K, T, r, DEFAULT_PARAMS, num_simulations=10000, num_time_steps=10)
    price_50k = heston_monte_carlo_price(S, K, T, r, DEFAULT_PARAMS, num_simulations=50000, num_time_steps=10)
    price_100k = heston_monte_carlo_price(S, K, T, r, DEFAULT_PARAMS, num_simulations=100000, num_time_steps=10)

    assert abs(price_50k - price_10k) > abs(price_100k - price_50k)