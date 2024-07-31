
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import yfinance as yf

tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "META", "TSLA", "JPM", "NVDA", "UNH"]

def predict_and_plot():
    recent_data = pd.read_csv("recent_data.csv", header=[0, 1], index_col=0)
    recent_data.columns = recent_data.columns.to_flat_index()

    predictions = {}
    actuals = {}
    
    for ticker in tickers:
        model = joblib.load(f"{ticker}_hmm.pkl")
        
        stock_data = recent_data.xs(ticker, level=1, axis=1)
        stock_data.dropna(inplace=True)
        
        stock_data['fracChange'] = (stock_data['Close'] - stock_data['Open']) / stock_data['Open']
        stock_data['fracHigh'] = (stock_data['High'] - stock_data['Open']) / stock_data['Open']
        stock_data['fracLow'] = (stock_data['Open'] - stock_data['Low']) / stock_data['Open']
        
        X = stock_data[['fracChange', 'fracHigh', 'fracLow']].values[-10:]
        
        hidden_states = model.predict(X)
        
        predicted_close = []
        for i in range(len(X)):
            next_state = model.transmat_[hidden_states[i]].argmax()
            mean_fracChange = model.means_[next_state][0]
            next_open = stock_data['Open'].iloc[i]
            predicted_close.append(next_open * (1 + mean_fracChange))
        
        predictions[ticker] = predicted_close
        actuals[ticker] = stock_data['Close'].values[-10:]
    
    plt.figure(figsize=(14, 10))
    
    for i, ticker in enumerate(tickers):
        plt.subplot(5, 2, i+1)
        plt.plot(actuals[ticker], label='Actual Close Price')
        plt.plot(predictions[ticker], label='Predicted Close Price')
        plt.title(f'{ticker} - Actual vs Predicted Close Prices')
        plt.xlabel('Days')
        plt.ylabel('Close Price')
        plt.legend()
        plt.grid(True)
    
    plt.tight_layout()
    plt.savefig("predicted_vs_actual.png")
    plt.show()

if __name__ == "__main__":
    predict_and_plot()
