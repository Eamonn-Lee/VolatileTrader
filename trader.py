import pandas as pd
from pprint import pprint

#single ticker monitor
class TickTrader:
    def __init__(self, ticker, init_capital, trailing_stop_pc, fetch):
        self.ticker = ticker        #
        self.init_cap = init_capital
        self.trailing_stop_percent = int(trailing_stop_pc) / 100 #decimal percentage drop stop

        self.cash = init_capital
        self.shares = 0

        self.highest_observed_price = 0
        self.trailing_stop_price = 0

        self.log = []
        self.data_fetch = fetch

    def fetch_curr_price(self, *args, **kwargs):
        """Getter: Ticker price, Swap with live data API"""
        return self.data_fetch(self.ticker, *args, **kwargs)
    
    def strategy(self, curr_date):
        curr_price = self.fetch_curr_price(curr_date)
        print(f"checking {curr_date}: {curr_price}")
        #holding shares
        if self.shares > 0: 
            if curr_price > self.highest_observed_price:
                #update and follow growth
                self.highest_observed_price = curr_price 
                self.trailing_stop_price = self.highest_observed_price * (1 - self.trailing_stop_percent)

            #if price is lower than highest observed but higher than stop: hold

            if curr_price < self.trailing_stop_price:
                #sell order
                self.sell(curr_date)

        #no shares
        elif self.cash > curr_price:
            #requires smarter buying
            self.buy(curr_date)

    def buy(self, date):
        #buying max shares
        price = self.fetch_curr_price(date)
        self.shares = self.cash // price 
        self.cash -= self.shares * price

        self.log.append((date, 'BUY', self.shares, price))    #would be better to use curr date, but needed for historical data


    def sell(self, date):
        #sell all
        price = self.fetch_curr_price(date)
        self.cash += self.shares * price
        self.reset_holdings()
        
        self.log.append((date, 'SELL', self.shares, price))

    def reset_holdings(self):
        #reset portfolio
        self.shares = 0
        self.highest_observed_price = 0
        self.trailing_stop_price = 0

    def view(self):
        total = self.cash + (self.shares * self.highest_observed_price)
        profit = total - self.init_cap
        return {
            "init": self.init_cap,
            "total": int(total),
            "curr_shares": int(self.shares),
            "profit": int(profit),
            "log": self.log
        }

if __name__ == "__main__":
    import yfinance as yf
    from datetime import datetime, timedelta

    ticker = "IBIT"
    init_cap = 1000
    trailing_stop_percentage = 5
    end = datetime.now()
    start = end - timedelta(days=6)
    interval = "1m"

    history = yf.Ticker(ticker).history(start=start, end=end, interval=interval)

    def test_fetch(ticker, dt):
        try:
            return history.loc[dt, 'Close']
        except KeyError:
            raise ValueError(f"Price @ {dt} not found")

    #init sim
    sim = TickTrader(ticker, init_cap, trailing_stop_percentage, test_fetch)

    for current_time, row in history.iterrows():
        try:
            sim.strategy(current_time)
        except ValueError as e: #catchall
            print(e)

    pprint(sim.view())

