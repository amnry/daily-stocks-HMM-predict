
import yfinance as yf
import pandas as pd

tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "GOOG"
           , "META", "TSLA", "JPM", "NVDA", "UNH"
           ]


data = yf.download(tickers=tickers, period="5yr")
data.to_csv("historical_data.csv")
