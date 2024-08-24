
import pandas as pd
from hmmlearn.hmm import GaussianHMM
import numpy as np
import joblib

tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "META", "TSLA", "JPM", "NVDA", "UNH"]

def train_hmm(data):
    # data = pd.read_csv("historical_data.csv", header=[0, 1], index_col=0)
    data.columns = data.columns.to_flat_index()
    
    for ticker in tickers:
        stock_data = data.xs(ticker, level=1, axis=1)
        stock_data.dropna(inplace=True)
        
        # Feature Engineering
        stock_data['fracChange'] = (stock_data['Close'] - stock_data['Open']) / stock_data['Open']
        stock_data['fracHigh'] = (stock_data['High'] - stock_data['Open']) / stock_data['Open']
        stock_data['fracLow'] = (stock_data['Open'] - stock_data['Low']) / stock_data['Open']
        
        X = stock_data[['fracChange', 'fracHigh', 'fracLow']].values
        
        model = GaussianHMM(n_components=4, covariance_type="diag", n_iter=1000)
        model.fit(X)
        
        joblib.dump(model, f"{ticker}_hmm.pkl")

if __name__ == "__main__":
    train_hmm()
