from src.market_data import get_market_data
from src.implied_volatility import compute_implied_vols
import matplotlib.pyplot as plt 

def market_implied_vol_curve(ticker: str) -> None:
    """
    Plots the implied volatility using market data of an option against strike prices.
    """
    
    S, T, chain_data  = get_market_data(ticker, 1)
    option_data = compute_implied_vols(S, T, 0.04, chain_data)
    option_data = option_data.dropna()
    plt.plot(option_data["strike"], option_data["implied_vol"])
    plt.xlabel("Strike prices")
    plt.ylabel("Implied volatility")
    plt.title("Market implied volatility curve")
    plt.grid(True)

    plt.savefig("figures/market_iv.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    market_implied_vol_curve("AAPL")