from src.parameters import HestonParameters 
from src.heston import characteristic_function
from scipy.integrate import quad
import numpy as np


def heston_call_price(
        S: float,
        K: float,
        T: float,
        r: float,
        params: HestonParameters,
    ) -> float:
    """
    Prices a European call option under the Heston stochastic volatility model using the 
    Gil-Pelaez Fourier inversion formula.

    Parameters:
        S (float): Current stock price.
        K (float): Strike price.
        T (float): Time to expiry in years.
        r (float): Continuously compounded risk-free interest rate.
        params (HestonParameters): Heston model parameters.

    Returns:
        float: The theoretical price of the call option under the Heston model.
    """
    
    P1 = 0.5 + (1 / np.pi) * quad(P1_integrand, 0, 100, args = (S, K, T, r, params))[0]

    P2 = 0.5 + (1 / np.pi) * quad(P2_integrand, 0, 100, args = (S, K, T, r, params))[0]

    return S * P1 - K * np.exp(-r*T) * P2

def P1_integrand(u: float, S: float, K: float, T: float, r: float, params: HestonParameters) -> float:
    """Integrand for the first risk-neutral probability P1 in the Gil-Pelaez formula."""
    phi = characteristic_function(u-1j, S, T, r, params)
    return np.real((np.exp(-1j * u * np.log(K)) * phi) / (1j * u * S))

def P2_integrand(u: float, S: float, K: float, T: float, r: float, params: HestonParameters) -> float:
    """Integrand for the second risk-neutral probability P2 in the Gil-Pelaez formula."""
    phi = characteristic_function(u, S, T, r, params)
    return np.real((np.exp(-1j * u * np.log(K)) * phi) / (1j * u))