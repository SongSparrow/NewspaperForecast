import pandas as pd
import matplotlib.pyplot as plt

w = 0.3
t = 0.3
d = 0.4
c = 1.8

train_set = pd.read_csv("raw_news_data.csv")


def train():
    train_set_title = train_set["title"]
    train_set_writer = train_set["writer"]
    train_set_date = train_set["date"]
    train_set_tags = train_set["tags"]
    length = len(train_set_title)

    title_hits = pd.read_csv("titles.csv", index_col="title")
    date_hits = pd.read_csv("dates.csv", index_col="date")
    writer_hits = pd.read_csv("writers.csv", index_col="writers")
    tag_hits = pd.read_csv("tags.csv", index_col="tags")

    title_score = 0
    result_date_score = []
    result_writer_score = []
    result_tag_score = []
    result_title_score = []
    result_title_i_score = []
    result = []
    for i in range(0, length):
        title_i = train_set_title.iloc[i]
        writer_i = train_set_writer.iloc[i]
        date_i = train_set_date.iloc[i]
        tag_i = train_set_tags.iloc[i]

        title_i_score = title_hits.loc[title_i]["hits_grade"]
        if str(type(title_i_score)) != "<class 'numpy.float64'>":
            title_i_score = title_hits.loc[title_i]["hits_grade"].mean()
            print(title_i_score)

        dirty_c_list = ["、", ":", "：", "（", "）", "；", "，", "/", ",", "("]
        for dirty_c in dirty_c_list:
            writer_i = writer_i.replace(dirty_c, " ")
        writer_i = writer_i.split()[0]
        writer_i_score = 0
        if writer_i in writer_hits["hits"]:
            writer_i_score = writer_hits.loc[writer_i]["hits_grade"]

        tag_i_list = []
        for dirty_c in dirty_c_list:
            tag_i.replace(dirty_c, " ")
        tags = tag_i.split()
        for tag in tags:
            if len(tag) > 1:
                tag_i_list.append(tag)
        _sum = 0
        j = 0
        for tag in tag_i_list:
            if tag in tag_hits["hits"]:
                _sum += tag_hits.loc[tag]["hits_grade"]
                j += 1
        tag_i_score = 0
        if j > 0:
            tag_i_score = _sum / j

        date_i = date_i[5:]
        date_i_score = date_hits.loc[date_i]["hits_grade"]

        result_date_score.append(date_i_score )
        result_tag_score.append(tag_i_score )
        result_writer_score.append(writer_i_score )
        result_title_i_score.append((date_i_score * d + tag_i_score * t + writer_i_score * w)*c)
        result_title_score.append(title_i_score)
        result.append((date_i_score * d + tag_i_score * t + writer_i_score * w)*c - title_i_score)
    result_df = pd.DataFrame({"date": result_date_score,
                        "tag": result_tag_score,
                        "writer": result_writer_score,
                        "title_i": result_title_i_score,
                        "title": result_title_score,
                        "result": result})
    print(result_df)
    # print(result_df.sum())

train()
