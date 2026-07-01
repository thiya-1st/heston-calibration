import yfinance as yf
from datetime import datetime
import pandas as pd

def get_market_data(ticker: str, expiry_choice: int) -> tuple[float, float, pd.DataFrame]:
    """
    Fetches option chain data for a given company and returns the data needed for calibration.

    Parameters:
        ticker (str): The ticker symbol of the company.
        expiry_choice (int): Which expiry to use.

    Returns:
        S (float): The current stock price.
        T (float): Time to expiry in years.
        info (pd.DataFrame): A DataFrame with columns:
            - strike: The strike prices of the call options.
            - market_price: The mid-price of the bid-ask spread.
    """

    company = yf.Ticker(ticker)
    expiry = company.options[expiry_choice]
    call_chain = company.option_chain(expiry).calls
    S = company.fast_info["lastPrice"]

    expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
    now = datetime.now()
    T = (expiry_date - now).total_seconds() / (365 * 24 * 60 * 60)

    strikes = call_chain["strike"]
    bids = call_chain["bid"]
    asks = call_chain["ask"]
    market_price = (bids + asks) / 2

    data = pd.DataFrame({
        "strike": strikes, 
        "market_price": market_price
    })

    return S, T, data
