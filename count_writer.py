import pandas as pd
import matplotlib.pyplot as plt

articles = pd.read_csv("raw_news_data.csv")
writers_and_hits = articles[["writer", "hits"]]
length = len(writers_and_hits)

writer_hit_list = []
dirty_c_list = ["、", ":", "：", "（", "）", "；", "，", "/", ",", "("]
for i in range(0, length):
    writer_str = writers_and_hits.iloc[i]["writer"]
    for dirty_c in dirty_c_list:
        writer_str = writer_str.replace(dirty_c, " ")
    writer = writer_str.split()[0]
    h = writers_and_hits.iloc[i]["hits"]
    writer_hit_list.append((writer, h))
writer_hit_list.sort()

length = len(writer_hit_list)
i = 0
writer_hit_u_list = []
while i < length:
    hit_sum = writer_hit_list[i][1]
    c = 1
    while i < length - 1 and writer_hit_list[i][0] == writer_hit_list[i + 1][0]:
        hit_sum += writer_hit_list[i + 1][1]
        c += 1
        i += 1
    writer_hit_u_list.append((writer_hit_list[i][0], hit_sum, c))
    i += 1

length = len(writer_hit_u_list)
writer_list = []
hit_list = []
count = []
for i in range(0, length):
    writer_list.append(writer_hit_u_list[i][0])
    hit_list.append(writer_hit_u_list[i][1])
    count.append(writer_hit_u_list[i][2])
tag_hit_dic = {
    "writers": writer_list,
    "hits": hit_list,
    "count": count
}
writer_hit_df = pd.DataFrame(tag_hit_dic)
writer_hit_df.to_csv("writers.csv",index=None)
writer_hit_df = writer_hit_df.sort_values(by="hits")
print(writer_hit_df)



