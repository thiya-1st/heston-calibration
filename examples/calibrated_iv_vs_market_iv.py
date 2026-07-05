from examples.calibrate_heston import optimise_heston
from src.market_data import get_market_data
from src.heston_pricing import heston_call_price
from src.parameters import params_vector_to_params
from src.implied_volatility import compute_implied_vols
import matplotlib.pyplot as plt

def calibrated_iv_vs_market_iv(ticker: str):
    S, T, data = get_market_data(ticker, 1)
    r = 0.05

    market_data = compute_implied_vols(S, T, r, data)
    market_data = market_data.dropna()
    plt.plot(market_data["strike"], market_data["implied_vol"], label = "Market")
    plt.xlabel("Strike prices")
    plt.ylabel("Implied volatility")
    plt.title("Market vs calibrated heston implied volatility curve")
    plt.grid(True)

    calibrated_params_vector, min_loss, rmse = optimise_heston(ticker)
    calibrated_params = params_vector_to_params(calibrated_params_vector)

    heston_prices = [heston_call_price(S, strike, T, r, calibrated_params) for strike in data["strike"]]
    heston_data = data.copy()
    heston_data["market_price"] = heston_prices
    heston_data = compute_implied_vols(S, T, r, heston_data)
    heston_data = heston_data.dropna()

    plt.plot(heston_data["strike"], heston_data["implied_vol"], label = "Heston")
    plt.legend()

    x_min = max(market_data["strike"].min(), heston_data["strike"].min())
    x_max = min(market_data["strike"].max(), heston_data["strike"].max())
    plt.xlim(x_min, x_max)

    visible_market = market_data[(market_data["strike"] >= x_min) & (market_data["strike"] <= x_max)]
    visible_heston = heston_data[(heston_data["strike"] >= x_min) & (heston_data["strike"] <= x_max)]
    y_min = min(visible_market["implied_vol"].min(), visible_heston["implied_vol"].min()) - 0.05
    y_max = max(visible_market["implied_vol"].max(), visible_heston["implied_vol"].max()) + 0.05
    plt.ylim(y_min, y_max)

    plt.show()
  
if __name__ == "__main__":
    calibrated_iv_vs_market_iv("AAPL")

