# visualize
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from datetime import datetime as dt

news_csv = pd.read_csv('raw_news_data.csv')


# assign everyday's hits to
def assign_hits_to_date(test_news):
    date_with_hits = {}
    for itemx in test_news.itertuples():
        date = getattr(itemx, 'date')
        hits = getattr(itemx, 'hits')

        if date_with_hits.get(date, 0) == 0:
            date_with_hits[date] = [[hits], 0]
        else:
            date_with_hits[date][0].append(hits)
    return date_with_hits


date_with_hits = assign_hits_to_date(news_csv)


# fill the dict with the delfault date
def fill_date_with_hits(start='2017-10-27', end='2020-05-19'):
    start_date = dt.strptime(start, '%Y-%m-%d').date()
    end_date = dt.strptime(end, '%Y-%m-%d').date()
    cur_date = start_date
    while (cur_date <= end_date):
        date = str(cur_date)
        if date_with_hits.get(date, 0) == 0:
            date_with_hits[date] = [[0], 0]
        cur_date += datetime.timedelta(days=1)


fill_date_with_hits()

import numpy as np

# compute the average
for key, value in date_with_hits.items():
    average_hits = int(0.5 + np.mean(value[0]))
    date_with_hits[key][1] = average_hits

# sort the dict by the key
sorted_date_with_hits = sorted(date_with_hits.items(), key=lambda item: item[0], reverse=False)


def plot_by_year(start_time, end_time):
    lenth_of_x = 0
    y = []
    # plot the line
    for item in sorted_date_with_hits:
        if (item[0] >= start_time) and (item[0] <= end_time):
            lenth_of_x += 1
            y.append(item[1][1])
    x = range(0, lenth_of_x)
    plt.figure(figsize=(20, 5))
    plt.plot(x, y)
    plt.scatter(x, y, marker='o', color='m', label='hits', s=20)
    plt.title(start_time + ' to ' + end_time)
    plt.legend()

    # plot the month number
    start = dt.strptime(start_time, '%Y-%m-%d').date()
    cur = start
    last_month = cur.month
    sig_12 = False
    for i in range(len(x)):
        cur = start + datetime.timedelta(days=x[i])
        cur_month = cur.month
        if (cur_month > last_month and not sig_12) or (cur_month < last_month):
            plt.annotate(str(cur_month), (x[i], 0), color='black', fontsize=20,
                         arrowprops=dict(facecolor='r', shrink=0.05))
            last_month = cur_month
            if last_month == 12:
                sig_12 = True
            else:
                sig_12 = False
    plt.show()


plot_by_year('2017-10-27', '2018-02-28')

plot_by_year('2018-03-01', '2018-08-31')

plot_by_year('2018-09-01', '2019-02-28')

plot_by_year('2019-03-01', '2019-08-31')

plot_by_year('2019-09-01', '2020-02-29')

plot_by_year('2020-03-01', '2020-05-19')