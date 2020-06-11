import pandas as pd
import matplotlib.pyplot as plt

# 加载并分割数据
articles = pd.read_csv("raw_news_data.csv")
tags_and_hits = articles[["tags", "hits"]]
# 得到条目数量
length = len(tags_and_hits)

tag_hit_list = []
dirty_chs = ["\"", "”", "“"]
replace_chs = ["、", ";"]
for i in range(0, length):
    # 去除标签中的脏字符
    tag_str = tags_and_hits.iloc[i]["tags"]
    for dirty_c in dirty_chs:
        tag_str = tag_str.replace(dirty_c, "")
    for replace_ch in replace_chs:
        tag_str = tag_str.replace(replace_ch, " ")
    # 将标签字符串分割
    tags = tag_str.split()
    # 记录下该标签字符串对应的点击量
    h = tags_and_hits.iloc[i]["hits"]
    for tag in tags:
        #  去除只有一个字符的标签
        if len(tag) > 1:
            # 存储标签与其对应的点击量
            tag_hit_list.append((tag, h))
# 按标签排序
tag_hit_list.sort()

length = len(tag_hit_list)
i = 0
tag_hit_u_list = []
while i < length:
    hit_sum = tag_hit_list[i][1]
    c = 1
    # 检查前后两个相同的标签并求和其点击量
    while i < length - 1 and tag_hit_list[i][0] == tag_hit_list[i + 1][0]:
        hit_sum += tag_hit_list[i + 1][1]
        c += 1
        i += 1
    # 将结果存储在tag_hit_u_list中
    tag_hit_u_list.append((tag_hit_list[i][0], hit_sum, c))
    i += 1

length = len(tag_hit_u_list)
tag_list = []
hit_list = []
count = []
# 构建DataFrame
for i in range(0, length):
    tag_list.append(tag_hit_u_list[i][0])
    hit_list.append(tag_hit_u_list[i][1])
    count.append(tag_hit_u_list[i][2])
tag_hit_dic = {
    "tags": tag_list,
    "hits": hit_list,
    "count": count
}
tag_hit_df = pd.DataFrame(tag_hit_dic)
tag_hit_df.to_csv("tags.csv")
# 按点击量排序
tag_hit_df = tag_hit_df.sort_values(by="hits")
print(tag_hit_df)

# tag_hit_df.plot.bar()
# plt.show()
