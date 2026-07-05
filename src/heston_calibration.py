from src.market_data import get_market_data
from src.heston_pricing import heston_call_price
from src.parameters import HestonParameters
import pandas as pd

def calibration_loss(
        S: float, 
        T: float, 
        r: float, 
        data: pd.DataFrame, 
        params_vector: list
    ) -> float:
    """
    
    """

    params = HestonParameters(
        v0 = params_vector[0],
        theta = params_vector[1],
        kappa = params_vector[2],
        xi = params_vector[3],
        rho = params_vector[4],
    )
    
    loss = 0
    for _, row in data.iterrows():
        heston_price = heston_call_price(S, row["strike"], T, r, params)
        error = heston_price - row["market_price"]
        loss += error**2

    return loss    

def calibration_rmse(S, T, r, data, params_vector):
    loss = calibration_loss(S, T, r, data, params_vector)
    return (loss / len(data))**0.5
    