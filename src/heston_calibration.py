from src.heston_pricing import heston_call_price
from src.parameters import params_vector_to_params
import pandas as pd

def calibration_loss(
        S: float, 
        T: float, 
        r: float, 
        data: pd.DataFrame, 
        params_vector: list
    ) -> float:
    """
    Computes the sum of squared errors between Heston model prices and market prices.

    Parameters:
        S (float): Current stock price.
        T (float): Time to expiry in years.
        r (float): Continuously compounded risk-free interest rate.
        data (pd.DataFrame): DataFrame with columns 'strike' and 'market_price'.
        params_vector (list): Heston parameters as a list [v0, theta, kappa, xi, rho].

    Returns:
        float: The sum of squared pricing errors across all options.
    """
    params = params_vector_to_params(params_vector)
    loss = 0
    for _, row in data.iterrows():
        heston_price = heston_call_price(S, row["strike"], T, r, params)
        error = heston_price - row["market_price"]
        loss += error**2
    return loss    

def calibration_rmse(
        S: float, 
        T: float, 
        r: float, 
        data: pd.DataFrame, 
        params_vector: list
    ) -> float:
    """
    Computes the root mean squared error between Heston model prices and market prices.

    Parameters:
        S (float): Current stock price.
        T (float): Time to expiry in years.
        r (float): Continuously compounded risk-free interest rate.
        data (pd.DataFrame): DataFrame with columns 'strike' and 'market_price'.
        params_vector (list): Heston parameters as a list [v0, theta, kappa, xi, rho].

    Returns:
        float: The root mean squared pricing error across all options.
    """
    loss = calibration_loss(S, T, r, data, params_vector)
    return (loss / len(data))**0.5