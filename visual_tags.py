import pandas as pd
import matplotlib.pyplot as plt

articles = pd.read_csv("raw_news_data.csv")
tags_and_hits = articles[["tags", "hits"]]
length = len(tags_and_hits)

tag_hit_list = []
for i in range(0, length):
    tag_str = tags_and_hits.iloc[i]["tags"]
    tag_str = tag_str.replace("\"", "")
    tag_str = tag_str.replace("“", "")
    tag_str = tag_str.replace("”", "")
    tag_str = tag_str.replace("、", " ")
    tag_str = tag_str.replace(";", " ")
    tags = tag_str.split()
    h = tags_and_hits.iloc[i]["hits"]
    for tag in tags:
        if len(tag) > 1:
            tag_hit_list.append((tag, h))
tag_hit_list.sort()

length = len(tag_hit_list)
i = 0
tag_hit_u_list = []
while i < length:
    hit_sum = tag_hit_list[i][1]
    while i<length-1 and tag_hit_list[i][0] == tag_hit_list[i + 1][0]:
        hit_sum += tag_hit_list[i + 1][1]
        i += 1
    tag_hit_u_list.append((tag_hit_list[i][0],hit_sum))
    i += 1

length = len(tag_hit_u_list)
tag_list = []
hit_list = []
for i in range(0,length):
    tag_list.append(tag_hit_u_list[i][0])
    hit_list.append(tag_hit_u_list[i][1])
tag_hit_dic = {
    "tags":tag_list[0:50],
    "hits":hit_list[0:50]
}
tag_hit_df = pd.DataFrame(tag_hit_dic)
tag_hit_df = tag_hit_df.sort_values(by="hits")
print(tag_hit_df)

tag_hit_df.plot.bar()
plt.show()




