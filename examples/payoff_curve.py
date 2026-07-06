import matplotlib.pyplot as plt
import numpy as np
from src.payoff import call_payoff

def plot_payoff(K: float, stock_low: float, stock_high: float, intervals: int) -> None:
    """
    Calculates the payoffs of several call options for different stock prices and plots the result.
    """
    stock_prices = np.linspace(stock_low, stock_high, intervals)
    payoffs = call_payoff(stock_prices, K)
    plt.plot(stock_prices, payoffs)
    plt.xlabel("Stock Price at Expiry (S_T)")
    plt.ylabel("Call Payoff")
    plt.title("Call Option Payoff Diagram")
    plt.grid(True)

    plt.savefig("figures/payoff_curve.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    plot_payoff(110, 50, 170, 1000)