import pandas as pd
import yfinance
import os
from stockstats import StockDataFrame

symbols = ["SPY", "AAPL"]
indicators = [
    "close_20_sma",
    "close_50_sma",
    "rsi",
    "macd",
    "boll_ub",
    "boll_lb",
]
data = pd.DataFrame()

for symbol in symbols:
    # Check if CSV file exists
    if not os.path.exists(os.path.join("../data", f"{symbol}.csv")):
        # Download the data
        df = yfinance.Ticker("SPY").history(period="max", interval="1d")

        # Save to CSV
        df.to_csv(os.path.join("../data", f"{symbol}.csv"))

    df = pd.read_csv(os.path.join("../data", f"{symbol}.csv"))

    # Rename Columns to lowercase
    df.columns = map(str.lower, df.columns)

    # Add Symbol Column
    df["tic"] = symbol

    # Convert to StockDataFrame for indicators
    stock = StockDataFrame.retype(df)

    # Add Indicators
    for indicator in indicators:
        try:
            stock[indicator]
        except:
            raise ValueError(f"Indicator {indicator} not found.")

    # Remove date from index
    stock = stock.reset_index()

    stock = stock[["date"] + indicators]

    # Rename columns to include symbol
    stock.columns = [f"{symbol}_{col}" if col != "date" else col for col in stock.columns]

    # Merge with data
    data = pd.merge(data, stock, left_index=True, right_index=True, how="outer")

# Remove 5 rows
data = data.iloc[5:]

# Drop NA
data = data.dropna()

# Reset index
data = data.reset_index()

# Remove time data from date
data["date"] = data["date"].apply(lambda x: x.split(" ")[0])

# Set date as index
data = data.set_index("date")

data.to_csv("./dataset/indicator_data.csv")