import numpy as np
import matplotlib.pyplot as plt

def call_payoff(S_T: np.ndarray | float, K: float) -> np.ndarray | float:
    """
    Calculate the payoff of a call option.

    Parameters:
        S_T (np.ndarray | float): The price(s) of the underlying asset at expiration.
        K (float): The strike price of the call option.

    Returns:
        np.ndarray | float: The payoff(s) of the call option. Returns an array if 
        S_T is an array, or a float if S_T is a scalar.
    """
    return np.maximum(S_T - K, 0)