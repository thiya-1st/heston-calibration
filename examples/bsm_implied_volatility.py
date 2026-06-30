import numpy as np
import matplotlib.pyplot as plt
from src.black_scholes import black_scholes_call
from src.implied_volatility import implied_volatility

def implied_vol_curve(
        S: float, 
        T: float, 
        r: float, 
        sigma: float, 
        strike_low: float, 
        strike_high: float,
        intervals: int,
    ) -> None:
    """
    Plots the implied volatility (calculated using BSM) of an option against strike prices.

    Parameters:
        S (float): Current stock price.
        T (float): Time to expiry in years.
        r (float): risk-free interest rate.
        sigma (float): volatility
        strike_low (float): Lower bound of strike price
        strike_high (float): Upper bound of strike_price
        intervals (int): Number of strike prices to use
    """
    strike_prices = np.linspace(strike_low, strike_high, intervals)
    option_prices = black_scholes_call(S, strike_prices, T, r, sigma)
    implied_vols = []
    valid_strikes = []
    for strike, option in zip(strike_prices, option_prices):
        try:
            implied_vol = implied_volatility(S, strike, T, r, option)
            implied_vols.append(implied_vol)
            valid_strikes.append(strike)
        except (ValueError, RuntimeError) as e:
            print(f"Failed for strike {strike}")
    plt.plot(valid_strikes, implied_vols)
    plt.xlabel("Strike prices")
    plt.ylabel("Implied volatility")
    plt.title("Implied volatility curve")
    plt.grid(True)
    plt.ylim(0, 0.5)
    plt.show()
    
if __name__ == "__main__":
    implied_vol_curve(100, 1, 0.05, 0.2, 80, 130, 1000)