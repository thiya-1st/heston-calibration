import numpy as np
import matplotlib.pyplot as plt

def call_payoff(S_T, K: float) -> float: 
    """
    Calculate the payoff of a call option.

    Parameters:
        S_T (float): The price of the underlying asset at expiration.
        K (float): The strike price of the call option.

    Returns:
        float: The payoff of the call option.
    """
    return np.maximum(S_T - K, 0)

def plot_payoff():
    """
    Calculates the payoffs of several call options for different stock prices and plots the result.
    """
    stock_prices = np.linspace(50, 170, 1000)
    K = 110
    payoffs = call_payoff(stock_prices, K)
    plt.plot(stock_prices, payoffs)
    plt.xlabel("Stock Price at Expiry (S_T)")
    plt.ylabel("Call Payoff")
    plt.title("Call Option Payoff Diagram")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    plot_payoff()