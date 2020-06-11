import pandas as pd
import matplotlib.pyplot as plt

title_list = pd.read_csv("raw_news_data.csv")[["title", "hits"]]
title_list.to_csv("titles.csv")


# 手动添加索引index


# visual

# title_list = pd.read_csv("titles.csv")

def visual_title_hits(start, end):
    title_hits = title_list["hits"].sort_values()[start:end]
    title_hits.plot(style=".")
    plt.show()


visual_title_hits(0, 1000)
visual_title_hits(1001, 2000)
visual_title_hits(2001, 3000)
visual_title_hits(3001, 4000)
visual_title_hits(4001, 5000)
visual_title_hits(5001, 6000)
visual_title_hits(6001, 7000)
visual_title_hits(7001, 8000)
visual_title_hits(8001, 9000)
visual_title_hits(9001, len(title_list) - 1)


def rate_title(title_hits):
    grade = title_hits / 60
    if grade > 100:
        grade = 100
    return grade


title_hits = title_list["hits"]
title_list.insert(2, "hits_grade", title_hits.apply(rate_title))
print(title_list)
title_list.to_csv("titles.csv")


def visual_title_rate(start, end):
    visual = title_list["hits_grade"].sort_values()[start:end]
    visual.plot(style=".")
    plt.show()


visual_title_rate(0, 9000)
