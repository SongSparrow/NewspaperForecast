import pandas as pd

articles = pd.read_csv("raw_news_data.csv")
writer_and_hits = articles[["writer","hits"]]
writer_list = []
for item in writer_and_hits["writer"].values:
    item = item.replace("、"," ")
    writer_list.append(item.split()[0])
writer_list = list(set(writer_list))
writer_list.sort()
print(writer_list)
print(len(writer_list))
