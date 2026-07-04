# Stocks

- A stock represents partial ownership of a company.
- The stock price is the current market value of one share.

# Options

- An option is a financial contract that gives the holder a right, but not an obligation, to buy or sell an underlying asset.
- Call option: the right (but not the obligation) to buy the underlying asset at the strike price before expiry (or at expiry for European options).
- Put option: the right (but not the obligation) to sell the underlying asset at the strike price before expiry (or at expiry for European options).

- Strike price: fixed price specified in the contract at which the holder has the right to buy (call) or sell (put) the stock at expiry (or before expiry for American options).
- Premium (option price): the market price paid today to purchase the option contract.
- Current stock price (S): the market price of the underlying stock today.
- Stock price at expiry (S_T): the market price of the underlying stock at the option's expiry date.

- Call payoff at expiry: max(S_T - K, 0).
- The premium paid today and the payoff received at expiry are different quantities.
- Profit = Payoff − Premium.

- An option chain is a table containing all available option contracts for a particular underlying stock and a particular expiry date.
- Each row represents a different strike price.
- For each strike price, the option chain contains the market premium of the corresponding call and put options.

## Market data
- Bid: highest price a buyer is currently willing to pay.
- Ask: lowest price a seller is currently willing to accept.
- Mid price = (Bid + Ask) / 2, often used as an estimate of the current market price.

## Synthetic (Black–Scholes) Curve
- Generated option prices using a constant volatility (e.g. σ = 0.2).
- Recovering the implied volatility from these prices gives a flat horizontal line at the original volatility.
- This verifies that the implied volatility solver works correctly.

## Market Implied Volatility Curve
- Uses real option prices from the market.
- The implied volatility varies with strike price, producing a volatility smile/skew rather than a flat line.
- This shows that the Black–Scholes assumption of constant volatility does not accurately describe real markets.

## Option Pricing as an Expected Payoff
- The price of an option is the discounted expected value of its payoff under the risk-neutral probability distribution.
- For a European call option: C = (e^-rt)E[max(S_T - K, 0)]

## Probability Distribution
- A probability distribution describes all possible future stock prices together with their probabilities.
- The option price depends on this distribution because the payoff depends on the future stock price.

### Black–Scholes
- Distribution is known analytically, it assumes the stock price follows a lognormal distribution.
- Allows the expected payoff to be calculated exactly, giving the closed-form Black–Scholes formula.

### Heston
- The Heston model is an extension of Black–Scholes where volatility is not constant.
- Volatility follows a stochastic (random) process, so the future stock price no longer has a simple lognormal distribution.
- The probability distribution becomes more flexible (e.g. skewed with fatter tails).
- This produces:
  - volatility skew (asymmetry)
  - volatility smile (fat tails)
  - better match to real market option prices
- Both Black–Scholes and Heston price options use the same expected-payoff equation. The difference is the probability distribution they assume for the future stock price.

## Heston Parameters
- v0: initial variance (starting volatility level squared)
- theta: long-term average variance (mean reversion level)
- kappa: speed of mean reversion (how fast volatility returns to theta)
- xi: volatility of volatility (how random volatility itself is)
- rho: correlation between stock price and volatility

## Characteristic Function

- In Heston, we do not directly model the probability distribution of S_T.
- Instead, we use the characteristic function φ(u), which encodes the distribution in Fourier space.
- The characteristic function is used because:
  - The density of S_T is hard to compute directly
  - Fourier methods allow option prices to be computed via integration

## Option Pricing in Heston

- The call price is still:

C = S P1 − K e^(−rT) P2

where P1 and P2 are probabilities computed using Fourier integrals:

- P1 = 1/2 + (1/π) ∫₀^∞ Re[ e^(−iu ln K) φ(u−i) / (iu S) ] du
- P2 = 1/2 + (1/π) ∫₀^∞ Re[ e^(−iu ln K) φ(u) / (iu) ] du

## Numerical Integration

- The integrals cannot be computed analytically.
- We approximate them using numerical integration (SciPy `quad`):

∫₀^∞ f(u) du ≈ ∫₀^Umax f(u) du

- In practice:
  - Umax ≈ 100 is used
  - This works because the integrand oscillates and decays for large u

## Implementation Structure

- characteristic_function(u): computes φ(u)
- P1_integrand(u): integrand for probability P1
- P2_integrand(u): integrand for probability P2
- heston_call_price(...): combines everything into final price

## Economic Interpretation

- Black–Scholes assumes a fixed probability distribution (lognormal).
- Heston assumes a stochastic volatility process, leading to a more flexible distribution.

Questions:
- arraylike?