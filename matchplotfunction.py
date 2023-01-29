#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np

import matplotlib.pyplot as plt

import yfinance as yf

# USEFUL_TICKERS = ["GOOG", "AAPL", "AMZN", "MSFT", "TSM", "NVDA", "TSLA", "JPM"]

def plot_matches(ticker, period, interval_length, interval_unit, segment_size, matches, future_depth):
    TICKER = ticker
    PERIOD = period
    INTERVAL_LENGTH=interval_length
    INTERVAL_UNIT=interval_unit
    INTERVAL=INTERVAL_LENGTH + INTERVAL_UNIT
    SEGMENT_SIZE = segment_size
    MATCHES = matches
    FUTURE_DEPTH = future_depth #how many periods to project into the future

    data = yf.Ticker(TICKER)

    historical_data = data.history(period=PERIOD, interval=INTERVAL)


    closes = list(historical_data['Open'])

    dates = list(historical_data.index)


    segments = []
    x = 0
    #create vectors of size SEGMENT_SIZE
    while x < len(closes) - 2*SEGMENT_SIZE - FUTURE_DEPTH: #dont want to include current segment
        curr_close = closes[x:x+SEGMENT_SIZE]
        segments.append(curr_close)
        x += 1


    # get future projections
    projections = []
    x = 0
    #create vectors of size SEGMENT_SIZE
    while x < len(closes) - 2*SEGMENT_SIZE - FUTURE_DEPTH: #same number as projections
        curr_projection = closes[x:x+SEGMENT_SIZE+FUTURE_DEPTH]
        projections.append(curr_projection)
        x += 1

    # create same vectors but with date information    
    date_segments = []
    x = 0
    while x < len(dates) - SEGMENT_SIZE:
        curr_date = dates[x:x+SEGMENT_SIZE]
        date_segments.append(curr_date)
        x += 1


    #normalize both segment and projection vectors using segment norm:
    for i in range(len(projections)):
        norm = np.linalg.norm(segments[i])
        for x in range(len(segments[i])):
            segments[i][x] = segments[i][x]/norm
        for x in range(len(projections[i])):
            projections[i][x] = projections[i][x]/norm

    # get most recent period
    period_length = str(SEGMENT_SIZE)+INTERVAL_UNIT
    curr_data = []
    curr_data = data.history(period=period_length, interval=INTERVAL)

    diff = SEGMENT_SIZE - len(curr_data)

    #if chopping/adding data, change segment size and query again
    if diff != 0:
        period_length = str(SEGMENT_SIZE + diff)+INTERVAL_UNIT
        curr_data = data.history(period=period_length, interval=INTERVAL)



    curr_close = list(curr_data['Open'])

    # normalize most recent period (don't think this is necessary)
    curr_norm = np.linalg.norm(curr_close)
    for i in range(len(curr_close)):
        curr_close[i] = curr_close[i] / curr_norm


    # find best dot match:


    #creates array of n pairs
    # first element of pair is the segment index
    # second index of the pair is the dot product
    best_dots = []

    for i in range(MATCHES):
        best_dots.append([0, 0])

    for i in range(0, len(segments)):
        dot = np.dot(curr_close, segments[i])
        entered = False # whether or not current value has been input into best_dots
        for x in range(len(best_dots)):
            #if matches are too close, only keep most accurate:
            if i - best_dots[x][0] < (SEGMENT_SIZE // 2):
                # only one survives
                if (dot > best_dots[x][1]) and not (entered):
                    best_dots[x][1] = dot
                    best_dots[x][0] = i
                entered = True

        for x in range(len(best_dots)):

            if (dot > best_dots[x][1]) and not (entered):
                best_dots[x][1] = dot
                best_dots[x][0] = i 
                entered = True



    def plot_historical(x, data):
        y = np.array(data)
        plt.plot(x, y, color='red', marker='o')




    #graph info
    plt.title(TICKER)
    plt.xlabel("Days")
    plt.ylabel("Normalized close price")


    #dummy line for legend:
    plt.plot([], [], color='red', marker='o', label='historical matches')

    #plot historical match (including projections)
    x_axis = range(len(projections[0])) # all segments have same size
    for match in best_dots:
        plot_historical(x_axis, projections[match[0]])

    #plot current data
    y1 = np.array(curr_close)
    x = range(len(y1))
    plt.plot(x, y1, color='black', marker='s', label = 'current prices')


    #plot average projection
    proj = []
    projection_x = range(len(projections[0]) - FUTURE_DEPTH, len(projections[0])) #list of x-values where value is projected

    #starts 1 prior to projections so that the current data connects
    total_x = range(len(projections[0]) - FUTURE_DEPTH - 1, len(projections[0])) 
    proj.append(curr_close[len(curr_close)-1])


    for i in projection_x:
        sum = 0
        for match in best_dots:
            sum += projections[match[0]][i]
        avg = sum / len(best_dots)
        proj.append(avg)


    #     line.append(curr_close[len(curr_close)-1])

    plt.plot(total_x, proj, color='blue', marker='D', label='future projection')




    plt.legend()
    plt.show()

