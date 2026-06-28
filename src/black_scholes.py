import numpy as np
from scipy.stats import norm

def black_scholes_call(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """
    Calculate the price of a European call option using the Black-Scholes model.

    Parameters:
        S (float): Current stock prices.
        K (float): The strike price of the call option.
        T (float): Time to expiry in years.
        r (float): risk-free interest rate.
        sigma (float): volatility

    Returns:
        C (float): Current price of call option.

    """

    d1 = (np.log(S/K) + (r+(sigma**2)/2)*T)/(sigma*(T**0.5))
    d2 = d1 - (sigma*(T**0.5))
    C = (S*norm.cdf(d1)) - (K*np.exp(-r*T)*norm.cdf(d2))
    return C

def implied_votality(S: float, K: float, T: float, r: float, C: float) -> float:
    
    return 0.01
