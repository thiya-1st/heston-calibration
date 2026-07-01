## Stocks

- A stock represents partial ownership of a company.
- The stock price is the current market value of one share.

## Options

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

- Bid: highest price a buyer is currently willing to pay.
- Ask: lowest price a seller is currently willing to accept.
- Mid price = (Bid + Ask) / 2, often used as an estimate of the current market price.

Questions:
- arraylike?