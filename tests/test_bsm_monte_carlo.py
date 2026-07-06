import pytest
from src.black_scholes import black_scholes_call
from src.monte_carlo import simulate_terminal_prices, monte_carlo_price, simulate_price_paths
import numpy as np

def test_monte_carlo_price_is_approx_black_scholes_price():
    S = 100
    K = 100
    T = 1
    r = 0.05
    sigma = 0.2

    bs_price = black_scholes_call(S, K, T, r, sigma)

    np.random.seed(42)
    terminal_prices = simulate_terminal_prices(S, T, r, sigma, 100000)
    mc_price = monte_carlo_price(K, T, r, terminal_prices)

    assert mc_price == pytest.approx(bs_price, abs = 0.03)

def test_monte_carlo_price_from_paths_is_approx_black_scholes_price():
    S = 100
    K = 100
    T = 1
    r = 0.05
    sigma = 0.2

    bs_price = black_scholes_call(S, K, T, r, sigma)

    np.random.seed(42)
    terminal_prices = simulate_price_paths(S, T, r, sigma, 100000, 1)[:, -1]
    mc_price = monte_carlo_price(K, T, r, terminal_prices)

    assert mc_price == pytest.approx(bs_price, abs = 0.03)