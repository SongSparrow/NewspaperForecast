import requests as rq
from pyquery import PyQuery as pq
import re
import csv
from datetime import datetime

url_max_page_code = 22000
url_min_page_code = 10000
max_date_time = datetime.strptime("2020-05-19", '%Y-%m-%d').date()
min_date_time = datetime.strptime("2017-10-27", '%Y-%m-%d').date()
url_head = 'https://news.cqu.edu.cn/newsv2/show-14-'
_headers = {
    "Cookies": "UM_distinctid=16f183f0e656d-0c44a277e897db-7711a3e-144000-16f183f0e66d; "
               "Hm_lvt_fbbe8c393836a313e189554e91805a69=1585301062,1585805916; "
               "Hm_lvt_bb57c1f66ec2fc27e393f9615bad47e5=1589206619,1590718273,1590719672; "
               "Hm_lpvt_bb57c1f66ec2fc27e393f9615bad47e5=1590720915",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.106 Safari/537.36"
}


#  检查html文档是否是新闻html
def not_exist(text):
    doc = pq(text)
    head_title = doc('h5').text()
    if head_title == '提示信息':
        return True
    return False


# 检查文章的发布日期有没有在指定日期内
def not_within_date(text_date):
    date = datetime.strptime(text_date, '%Y-%m-%d').date()
    if (date > max_date_time) or (date < min_date_time):
        return True
    return False


# 获取对应url的html文档
def get_web_page(url):
    request_source = rq.get(url, headers=_headers)
    return request_source.text


# 获取全部文章的url
def get_all_url(start_code, end_code):
    all_the_url = []
    for i in range(start_code, end_code + 1):
        url_realistic = url_head + str(i) + '-1.html'
        all_the_url.append(url_realistic)
    return all_the_url


# 获取文章的属性信息
def get_article(page):
    if not_exist(page):
        return None
    document = pq(page)

    # get date
    date_text = document(".ibox span").text()
    date_str = date_text.split(":")
    date = date_str[1].strip()
    # if the date is out of the limitation
    if not_within_date(date):
        return None

    article_elements = []
    # get title
    title = document('h1').text()

    # get writer
    writer = "无名氏"
    writer_nodes = document(".dinfoa")
    if writer_nodes.find("span").text() == "作者 :":
        writer = writer_nodes.find("a").text()

    # get tags
    tag_nodes = document(".tags")
    tags = "Nothing"
    if tag_nodes.find("span").text() == "相关热词搜索 :":
        tags = tag_nodes.find("a").text()
        if str.find(tags, "，") != -1:
            tags = tags.replace("，", " ")
        if str.find(tags, ";"):
            tags = tags.replace(";", " ")

    # get hits
    hits_link = document("script[language=JavaScript]").attr.src
    data_text = rq.get(hits_link, headers=_headers).text
    hits = re.findall("[0-9]+", data_text)[-1]

    article_elements.append(title)
    article_elements.append(writer)
    article_elements.append(date)
    article_elements.append(tags)
    article_elements.append(hits)

    return article_elements


# 将文章的属性信息存储下来
def store_in_csv(file_name):
    csv_file = open(file_name, "w", newline='', encoding='utf-8-sig')
    writer = csv.writer(csv_file)
    writer.writerow(["title", "writer", "date", "tags", "hits"])
    all_the_urls = get_all_url(url_min_page_code, url_max_page_code)
    print(all_the_urls)
    for url_item in all_the_urls:
        web_page_text = get_web_page(url_item)
        classify_article = get_article(web_page_text)
        if classify_article is None:
            continue
        writer.writerow(classify_article)


store_in_csv('raw_news_data.csv')

#visualize
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from datetime import datetime as dt


news_csv=pd.read_csv('raw_news_data.csv')

#assign everyday's hits to 
def assign_hits_to_date(test_news):
    date_with_hits={}
    for itemx in test_news.itertuples():
        date=getattr(itemx,'date')
        hits=getattr(itemx,'hits')

        if date_with_hits.get(date,0)==0:
            date_with_hits[date]=[[hits],0]
        else:
            date_with_hits[date][0].append(hits)
    return date_with_hits

date_with_hits=assign_hits_to_date(news_csv)

#fill the dict with the delfault date
def fill_date_with_hits(start='2017-10-27',end='2020-05-19'):
    start_date=dt.strptime(start,'%Y-%m-%d').date()
    end_date=dt.strptime(end,'%Y-%m-%d').date()
    cur_date=start_date
    while(cur_date<=end_date):
        date=str(cur_date)
        if date_with_hits.get(date,0)==0:
            date_with_hits[date]=[[0],0]
        cur_date+=datetime.timedelta(days=1)
            
        
fill_date_with_hits()    

import numpy as np
#compute the average
for key,value in date_with_hits.items():
    average_hits=int(0.5+np.mean(value[0]))
    date_with_hits[key][1]=average_hits


#sort the dict by the key
sorted_date_with_hits=sorted(date_with_hits.items(),key=lambda item:item[0], reverse=False)

def plot_by_year(start_time,end_time):
    lenth_of_x=0
    y=[]
    #plot the line
    for item in sorted_date_with_hits:
        if (item[0]>=start_time) and (item[0]<=end_time):
            lenth_of_x+=1
            y.append(item[1][1])
    x=range(0,lenth_of_x)    
    plt.figure(figsize=(20,5))
    plt.plot(x,y)
    plt.scatter(x, y, marker = 'o', color = 'm', label='hits', s = 20)
    plt.title(start_time+' to '+end_time)
    plt.legend()
    
    #plot the month number
    start=dt.strptime(start_time,'%Y-%m-%d').date()
    cur=start
    last_month=cur.month
    sig_12=False
    for i in range(len(x)):
        cur=start+datetime.timedelta(days=x[i])
        cur_month=cur.month
        if (cur_month>last_month and not sig_12) or (cur_month<last_month):
            plt.annotate(str(cur_month),(x[i],0),color='black',fontsize=20,arrowprops=dict(facecolor='r', shrink=0.05))
            last_month=cur_month
            if last_month==12:
                sig_12=True
            else:
                sig_12=False
    plt.show()

plot_by_year('2017-10-27','2018-02-28')

plot_by_year('2018-03-01','2018-08-31')

plot_by_year('2018-09-01','2019-02-28')

plot_by_year('2019-03-01','2019-08-31')

plot_by_year('2019-09-01','2020-02-29')

plot_by_year('2020-03-01','2020-05-19')