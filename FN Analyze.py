import numpy as np
import pandas as pd
import random

#Simulate stock price data for 5 stocks over 4 months
def simulate_stock_prices(n_stocks=5, n_days=120):
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'][:n_stocks]
    prices = {
        ticker: np.cumprod(1 + np.random.normal(0.0005, 0.02, n_days)) * 100
        for ticker in tickers }
    return pd.DataFrame(prices)

# Computation 
def analyze_portfolio(prices_df):
    returns = prices_df.pct_change().dropna()
    cumulative_returns = (1 + returns).cumprod()

    mean_returns = returns.mean() * 365  # Annualized
    volatility = returns.std() * np.sqrt(365)
    summary = pd.DataFrame({
        'Annualized Return (%)': mean_returns * 100,
        'Annualized Volatility (%)': volatility * 100
    })
    summary['Return/Risk Ratio'] = summary['Annualized Return (%)'] / summary['Annualized Volatility (%)']
    summary['Recommendation'] = summary['Return/Risk Ratio'].apply(
        lambda x: 'Buy' if x == summary['Return/Risk Ratio'].max() else ('Sell' if x == summary['Return/Risk Ratio'].min() else 'Hold')
    )
    return summary.round(2)

# look like GPT-style
def generate_commentary(summary_df):
    comments = []
    for idx, row in summary_df.iterrows():
        comment = f"{idx}: Expected return of {row['Annualized Return (%)']:.2f}%, volatility of {row['Annualized Volatility (%)']:.2f}%. Recommendation: {row['Recommendation']}."
        comments.append(comment)
    return "\n".join(comments)

if __name__ == '__main__':
    prices = simulate_stock_prices()
    summary = analyze_portfolio(prices)
    print("\n=== Portfolio Analysis Summary ===\n")
    print(summary)
    print("\n=== GPT Commentary ===\n")
    print(generate_commentary(summary))
