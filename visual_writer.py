import pandas as pd
import matplotlib.pyplot as plt

articles = pd.read_csv("raw_news_data.csv")
writers_and_hits = articles[["writer", "hits"]]
length = len(writers_and_hits)

writer_hit_list = []
for i in range(0, length):
    writer_str = writers_and_hits.iloc[i]["writer"]
    writer_str = writer_str.replace("、", " ")
    writer = writer_str.split()[0]
    h = writers_and_hits.iloc[i]["hits"]
    writer_hit_list.append((writer, h))
writer_hit_list.sort()

length = len(writer_hit_list)
i = 0
writer_hit_u_list = []
while i < length:
    hit_sum = writer_hit_list[i][1]
    while i<length-1 and writer_hit_list[i][0] == writer_hit_list[i + 1][0]:
        hit_sum += writer_hit_list[i + 1][1]
        i += 1
    writer_hit_u_list.append((writer_hit_list[i][0],hit_sum))
    i += 1

length = len(writer_hit_u_list)
writer_list = []
hit_list = []
for i in range(0,length):
    writer_list.append(writer_hit_u_list[i][0])
    hit_list.append(writer_hit_u_list[i][1])
tag_hit_dic = {
    "tags":writer_list[0:50],
    "hits":hit_list[0:50]
}
writer_hit_df = pd.DataFrame(tag_hit_dic)
writer_hit_df = writer_hit_df.sort_values(by="hits")
print(writer_hit_df)

writer_hit_df.plot.bar()
plt.show()




