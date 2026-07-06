from src.parameters import HestonParameters 
from src.heston import characteristic_function
from src.monte_carlo import simulate_heston_paths, monte_carlo_price
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

def heston_monte_carlo_price(
        S: float, 
        K: float, 
        T: float, 
        r: float, 
        params: HestonParameters, 
        num_simulations: int, 
        num_time_steps: int
    ) -> float:
    """
    Prices a European call option under the Heston model using Monte Carlo simulation.

    Parameters:
        S (float): Current stock price.
        K (float): Strike price.
        T (float): Time to expiry in years.
        r (float): Continuously compounded risk-free interest rate.
        params (HestonParameters): Heston model parameters (kappa, theta, xi, rho, v0).
        num_simulations (int): Number of simulated paths to generate.
        num_time_steps (int): Number of time steps per path.

    Returns:
        float: The estimated price of the call option under the Heston model.
    """

    price_paths, _ = simulate_heston_paths(S, T, r, params, num_simulations, num_time_steps)
    terminal_prices = price_paths[:, -1]
    return monte_carlo_price(K, T, r, terminal_prices)
