import yfinance as yf
from datetime import datetime, timedelta


class test_api:
    def __init__(self, ticker, start, end, interval):
        self.ticker = ticker
        self.index = 0
        self.history = yf.Ticker(ticker).history(start=start, end=end, interval=interval)
        self.interval = interval

    def fetch(self):
        if self.index < len(self.history):
            price = self.history.iloc[self.index]['Close']
            self.index += 1
            return price
        else:
            raise StopIteration("End of history reached")
        

t = test_api("IBIT", (datetime.now() - timedelta(days=6)), (datetime.now()), "1m")

for i in range(30):
    print(t.fetch())
