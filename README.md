# match-plot-function
Matches current stock period data to historical charts


This module leverages the Yahoo Finance API through the publicly available yfinance library to analyze up to approximately 3,000 points of historical data (exact Yahoo Finance data limit varies by period) and find any number of matches for a given ticker.  These best fitting plots are then plotted alongside the current period, and an estimated projection of future values.

## plot_matches()
The plot_matches function takes the following parameters:
ticker - stock ticker symbol, e.g. 'GOOG'
period - full period over which analyses is conducted (limited by Yahoo Finance data limits)
interval_length - length of each interval period
interval_unit - unit of intervals
segment_size - number of intervals observed
matches - number of matching plots returned
future_depth - how far to project into future
ex: mpf.plot_matches('TSM', '7d', '1', 'm', 21, 10, 10)
