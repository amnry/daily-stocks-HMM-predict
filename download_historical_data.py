
import yfinance as yf
import pandas as pd

tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "META", "TSLA", "JPM", "NVDA", "UNH"]

def download_data(tickers, period="5y"):
    data = yf.download(tickers=tickers, period=period)
    data.to_csv("historical_data.csv")

if __name__ == "__main__":
    download_data(tickers)
