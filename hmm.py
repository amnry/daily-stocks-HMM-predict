import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from hmmlearn.hmm import GaussianHMM

import warnings
warnings.filterwarnings('ignore')


# Clean up the columns and index
data = data.reset_index()  # Reset index to work with columns
data.columns = data.columns.str.replace(' ', '')
data.set_index(['Date', 'Ticker'], inplace=True)  # Set the index back

# Filter to get the last 15 market days
data = data.groupby(level='Ticker').tail(15)

# Prepare to store the predictions and actual prices for plotting
predicted_close_prices = {}
actual_close_prices = {}

# Loop through each ticker to train HMM and predict prices
for ticker in tickers:
    stock_data = data.xs(ticker, level='Ticker')
    
    # Calculate fractional changes
    stock_data['fracChange'] = (stock_data['Close'] - stock_data['Open']) / stock_data['Open']
    stock_data['fracHigh'] = (stock_data['High'] - stock_data['Open']) / stock_data['Open']
    stock_data['fracLow'] = (stock_data['Open'] - stock_data['Low']) / stock_data['Open']
    
    # Discretize the data
    nfc, nfh, nfl = 50, 10, 10
    fracChange_bins = np.linspace(stock_data['fracChange'].min(), stock_data['fracChange'].max(), nfc)
    fracHigh_bins = np.linspace(stock_data['fracHigh'].min(), stock_data['fracHigh'].max(), nfh)
    fracLow_bins = np.linspace(stock_data['fracLow'].min(), stock_data['fracLow'].max(), nfl)
    
    stock_data['disc_fracChange'] = np.digitize(stock_data['fracChange'], fracChange_bins)
    stock_data['disc_fracHigh'] = np.digitize(stock_data['fracHigh'], fracHigh_bins)
    stock_data['disc_fracLow'] = np.digitize(stock_data['fracLow'], fracLow_bins)
    
    # Combine the discretized features into a single state space
    stock_data['state'] = (stock_data['disc_fracLow'] - 1) * (nfc * nfh) + (stock_data['disc_fracHigh'] - 1) * nfc + stock_data['disc_fracChange']
    
    # Prepare training data
    X = stock_data[['fracChange', 'fracHigh', 'fracLow']].values
    
    # Train the HMM
    model = GaussianHMM(n_components=4, covariance_type="diag", n_iter=1000)
    model.fit(X)
    
    # Predict the stock prices for the last 5 days
    n_days = 5
    bin_size = 10
    predicted_close = []
    
    for i in range(len(stock_data) - n_days, len(stock_data)):
        recent_data = X[i-bin_size:i]
        hidden_states = model.predict(recent_data)
        
        # Predict the next day's state
        next_state = model.transmat_[hidden_states[-1]].argmax()
        mean_fracChange = model.means_[next_state][0]
        
        next_open = stock_data['Open'].iloc[i]
        predicted_close.append(next_open * (1 + mean_fracChange))
    
    # Store the actual and predicted prices
    predicted_close_prices[ticker] = predicted_close
    actual_close_prices[ticker] = stock_data['Close'].iloc[-n_days:].values
