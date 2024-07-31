
import yfinance as yf
import pandas as pd

tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "META", "TSLA", "JPM", "NVDA", "UNH"]

def download_recent_data(tickers, period="10d"):
    data = yf.download(tickers=tickers, period=period)
    data.to_csv("recent_data.csv")

if __name__ == "__main__":
    download_recent_data(tickers)
