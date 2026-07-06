from src.market_data import get_market_data
from src.heston_calibration import calibration_loss, calibration_rmse
from scipy.optimize import minimize
import numpy as np

def optimise_heston(ticker: str) -> tuple[np.ndarray, float, float]:
    """
    Calibrates Heston model parameters to market option prices using L-BFGS-B optimisation.
    """
    S, T, data = get_market_data(ticker, 1)
    r = 0.05
    x0 = [0.04, 0.04, 2, 0.3, -0.7] # initial values

    bounds = [
    (0.001, 1),     # v0
    (0.001, 1),     # theta
    (0.01, 10),     # kappa
    (0.01, 5),      # xi
    (-0.99, 0.99),  # rho
    ]

    def objective(params_vector):
        return calibration_loss(S, T, r, data, params_vector)

    result = minimize(objective, x0 = x0, bounds = bounds, method="L-BFGS-B")
    rmse = calibration_rmse(S, T, r, data, result.x)

    return result.x, result.fun, rmse

if __name__ == "__main__":
    calibrated_params, min_loss, rmse = optimise_heston("AAPL")
    print(f"Calibrated parameters: {calibrated_params}")
    print(f"Minimal loss: {min_loss}")
    print(f"RMSE: {rmse}")