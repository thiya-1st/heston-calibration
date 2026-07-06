import numpy as np
from src.payoff import call_payoff
from src.parameters import HestonParameters

def simulate_terminal_prices(
        S: float, 
        T: float, 
        r: float, 
        sigma: float, 
        num_simulations: int
    ) -> np.ndarray:
    """
    Simulates terminal stock prices under geometric Brownian motion using the Black-Scholes model.

    Parameters:
        S (float): Current stock price.
        T (float): Time to expiry in years.
        r (float): Continuously compounded risk-free interest rate.
        sigma (float): Volatility of the underlying asset.
        num_simulations (int): Number of simulated terminal prices to generate.

    Returns:
        np.ndarray: Array of simulated terminal stock prices at time T.
    """
    random_variables = np.random.normal(0, 1, num_simulations)
    terminal_prices = S * np.exp(T*(r-0.5*sigma**2) + sigma*random_variables*np.sqrt(T))

    return terminal_prices

def monte_carlo_price(K: float, T: float, r: float, terminal_prices: np.ndarray) -> float:
    """
    Estimates the price of a European call option using Monte Carlo simulation.

    Parameters:
        K (float): Strike price of the call option.
        T (float): Time to expiry in years.
        r (float): Continuously compounded risk-free interest rate.
        terminal_prices (np.ndarray): Array of simulated terminal stock prices.

    Returns:
        float: The estimated price of the call option.
    """
    average_payoff = np.mean(call_payoff(terminal_prices, K))
    discounted_payoff = np.exp(-r*T) * average_payoff
    return discounted_payoff

def simulate_price_paths(
        S: float, 
        T: float, 
        r: float, 
        sigma: float, 
        num_simulations: int,
        num_time_steps: int
    ) -> np.ndarray:
    """
    Simulates stock price paths under geometric Brownian motion.

    Parameters:
        S (float): Current stock price.
        T (float): Time to expiry in years.
        r (float): Continuously compounded risk-free interest rate.
        sigma (float): Volatility of the underlying asset.
        num_simulations (int): Number of simulated price paths to generate.
        num_time_steps (int): Number of time steps per path.

    Returns:
        np.ndarray: Array of shape (num_simulations, num_time_steps + 1) containing
        simulated price paths. Each row is one path, each column is a time step,
        with column 0 being the initial price S.
    """
    
    delta_t = T / num_time_steps
    price_paths = np.zeros((num_simulations, num_time_steps + 1))
    price_paths[:, 0] = S
    random_variables = np.random.normal(0, 1, (num_simulations, num_time_steps))

    for t in range(num_time_steps):
        price_paths[:, t+1] = (
            price_paths[:, t] 
            * np.exp(delta_t*(r-0.5*sigma**2) + sigma*random_variables[:, t]*np.sqrt(delta_t))
        )

    return price_paths

def simulate_heston_paths(
        S: float, 
        T: float, 
        r: float, 
        params: HestonParameters, 
        num_simulations: int,
        num_time_steps: int
    ) -> tuple[np.ndarray, np.ndarray]:
    """
    Simulates stock price and variance paths under the Heston stochastic volatility model
    using the Euler-Maruyama discretisation with full truncation.

    Parameters:
        S (float): Current stock price.
        T (float): Time to expiry in years.
        r (float): Continuously compounded risk-free interest rate.
        params (HestonParameters): Heston model parameters (kappa, theta, xi, rho, v0).
        num_simulations (int): Number of simulated paths to generate.
        num_time_steps (int): Number of time steps per path.

    Returns:
        tuple[np.ndarray, np.ndarray]: A tuple of two arrays each of shape
        (num_simulations, num_time_steps + 1). The first contains simulated stock 
        price paths, the second contains simulated variance paths.
    """
    delta_t = T / num_time_steps
    price_paths = np.zeros((num_simulations, num_time_steps + 1))
    variance_paths = np.zeros((num_simulations, num_time_steps + 1))
    price_paths[:, 0] = S
    variance_paths[:, 0] = params.v0

    z1 = np.random.normal(0, 1, (num_simulations, num_time_steps))
    z2 = np.random.normal(0, 1, (num_simulations, num_time_steps))
    Ws = z1
    Wv = z1 * params.rho + z2 * np.sqrt(1-params.rho**2)

    for t in range(num_time_steps):
        prev_vars = np.maximum(variance_paths[:, t], 0)
        variance_paths[:, t+1] = (
            prev_vars 
            + params.kappa * (params.theta - prev_vars) * delta_t
            + params.xi * np.sqrt(prev_vars * delta_t) * Wv[:, t]
        )
        price_paths[:, t+1] = (
            price_paths[:, t] 
            * np.exp(delta_t*(r-0.5*prev_vars) + np.sqrt(prev_vars * delta_t) * Ws[:, t])
        )
    
    return price_paths, variance_paths
        
