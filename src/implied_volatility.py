from src.black_scholes import black_scholes_call
import pandas as pd

def implied_volatility(
        S: float, 
        K: float, 
        T: float, 
        r: float, 
        market_price: float, 
        vol_low: float = 0.001,
        vol_high: float = 3.0,
        tolerance: float = 1e-6, 
        max_iterations: int = 100
    ) -> float:
    """
    Calculates the implied volatility of an option using the bisection method.
    Uses the tolerance and max_iterations to know when to stop the bisection method.

    Parameters:
        S (float): Current stock price.
        K (float): The strike price of the call option.
        T (float): Time to expiry in years.
        r (float): risk-free interest rate.
        market_price (float): Current market price of the call option.
        vol_low (float): Initial lower bound of volatility.
        vol_high (float): Initial higher bound of volatility.
        tolerance (float): The acceptable difference between the Black-Scholes price and the market price before stopping.
        max_iterations (int): Maximum number of iterations before the algorithm stops.

    Returns:
        float: The implied volatility.
    """
    bs_low = black_scholes_call(S, K, T, r, vol_low)
    bs_high = black_scholes_call(S, K, T, r, vol_high)
    f_low = bs_low - market_price
    f_high = bs_high - market_price
    if abs(f_low) < tolerance:
        return vol_low
    elif abs(f_high) < tolerance:
        return vol_high
    elif f_low < 0 and f_high > 0: # As volatility increases, f increases
        for i in range(max_iterations):
            vol_mid = (vol_low + vol_high)/2
            bs_mid = black_scholes_call(S, K, T, r, vol_mid)
            f_mid = bs_mid - market_price
            if abs(f_mid) < tolerance:
                return vol_mid
            elif f_mid < 0:
                vol_low = vol_mid
            else:
                vol_high = vol_mid
        raise RuntimeError("Maximum number of iterations reached.")
    else:
        raise ValueError("Root is not bracketed by the initial volatility bounds.")

def compute_implied_vols(S: float, T: float, r: float, data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the implied volatility for each option in the DataFrame and appends 
    it as a new column.

    Parameters:
        S (float): The current stock price.
        T (float): Time to expiry in years.
        r (float): The continuously compounded risk-free interest rate.
        data (pd.DataFrame): A DataFrame with columns:
            - strike: The strike prices of the call options.
            - market_price: The mid-price of the bid-ask spread.

    Returns:
        data (pd.DataFrame): The input DataFrame with an additional column:
            - implied_vol: The implied volatility for each option, or NaN if it 
              could not be computed.
    """
    implied_vols = []
    for _, row in data.iterrows():
        try:
            implied_vol = implied_volatility(S, row["strike"], T, r, row["market_price"])
        except (ValueError, RuntimeError):
            implied_vol = None
        implied_vols.append(implied_vol)
    data["implied_vol"] = implied_vols

    return data