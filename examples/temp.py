from src.heston_pricing import heston_call_price
from src.parameters import HestonParameters
from src.black_scholes import black_scholes_call

DEFAULT_PARAMS = HestonParameters(
    v0 = 0.04,
    theta = 0.04,
    kappa = 2,
    xi = 0.3,
    rho = -0.7,
)

price = heston_call_price(100, 100, 1, 0.05, DEFAULT_PARAMS)
print(price)

bs_price = black_scholes_call(S=100, K=100, T=1, r=0.05, sigma=0.2)
print(bs_price)