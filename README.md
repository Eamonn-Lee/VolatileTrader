# Trailing Stop Loss Order Simulator

A simulator for **Trailing Stop Loss Orders**, designed as a trading strategy for volatile stocks. 

- Implements a percentage-based trailing stop mechanism to maximize profits and minimize losses.
  - Dynamically adjusts the trailing stop price based on the highest observed stock price.


- Uses `yfinance` to fetch historical stock price data for backtesting.
  - Designed to integrate with real-time stock price API for live simulations. Replace the data-fetching function with preferred API.
