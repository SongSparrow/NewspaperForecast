import pandas as pd
import matplotlib.pyplot as plt


def get_average_hits(file):
    data = pd.read_csv(file)
    length = len(data)
    data_level = []
    for i in range(0, length):
        data_level.append(data.iloc[i]["hits"] / data.iloc[i]["count"])
    data_level = pd.Series(data_level)
    return data, data_level


# writers
writers, writers_avg_hits = get_average_hits("writers.csv")
writers_avg_hits.plot()
plt.show()


def rate_writers(_writer_level):
    grade = _writer_level / 15
    if grade > 100:
        grade = 100
    return grade


writers.insert(2, "hits_grade", writers_avg_hits.apply(rate_writers))
writers = writers.sort_values(by="hits_grade")
visual = writers["hits_grade"]
visual.plot()
plt.show()
writers.to_csv("writers.csv")
print(writers)

# tags
tags, tag_level = get_average_hits("tags.csv")
tag_level.plot()
plt.show()


def rate_tags(hits):
    grade = hits * 5 / 100
    if grade > 100:
        grade = 100
    return grade


tags.insert(3, "hits_grade", tag_level.apply(rate_tags))
tags = tags.sort_values(by="hits_grade")
visual = tags["hits_grade"]
visual.plot()
plt.show()
tags.to_csv("tags.csv", index=None)
print(tags)


# date
def rate_dates(date_hits):
    grade = date_hits / 25
    if grade > 100:
        grade = 100
    return grade


date = pd.read_csv("dates.csv")
date = date.sort_values(by="date")
length = len(date)
i = 0
date_list = []
date_hits_list = []
while i < length:
    sum = date.iloc[i]["avg_hits"]
    c = 1
    while i < length - 1 and date.iloc[i]["date"] == date.iloc[i + 1]["date"]:
        sum += date.iloc[i + 1]["average_hits"]
        c += 1
        i += 1
    date_list.append(date.iloc[i]["date"])
    date_hits_list.append(int(round(sum / c)))
    i += 1
date_df = pd.DataFrame({"date": date_list, "avg_hits": date_hits_list})
date_df["avg_hits"].plot()
plt.show()
date_df.insert(2, "hits_grade", date_df["avg_hits"].apply(rate_dates))
date_df.to_csv("dates.csv", index=None)
date_df["hits_grade"].plot()
plt.show()
print(date_df)
# 2018-02-12,20870
