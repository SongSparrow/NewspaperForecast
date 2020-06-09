import requests as rq
from pyquery import PyQuery as pq
import re
import csv
from datetime import datetime

url_max_page_code = 22000
url_min_page_code = 10000
max_date_time = datetime.strptime("2020-05-19", '%Y-%m-%d').date()
min_date_time = datetime.strptime("2019-10-27", '%Y-%m-%d').date()
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
    article_elements = []
    # get title
    title = document('h1').text()
    # get writer
    writer_nodes = document(".dinfoa").find("a")
    writer = writer_nodes.text(" ")
    # get date
    date_text = document(".ibox span").text()
    date_str = date_text.split(":")
    date = date_str[1].strip()
    # get content
    content = document(".acontent").text()
    # get tags
    tag_nodes = document(".tags").find("a")
    tags = tag_nodes.text(" ")
    # get hits
    hits_link = document("script[language=JavaScript]").attr.src
    data_text = rq.get(hits_link, headers=_headers).text
    hits = re.findall("[0-9]+", data_text)[-1]
    # generally the size of content will be less than 5 when the article is transmitted
    # if the date is out of the limitation
    if (len(content) < 5) or not_within_date(date):
        return None

    article_elements.append(title)
    article_elements.append(writer)
    article_elements.append(date)
    article_elements.append(content)
    article_elements.append(tags)
    article_elements.append(hits)

    return article_elements


# 将文章的属性信息存储下来
def store_in_csv(file_name):
    csv_file = open(file_name, "w", newline='', encoding='utf-8-sig')
    writer = csv.writer(csv_file)
    writer.writerow(["title", "writer", "date", "content", "tags", "hits"])
    all_the_urls = get_all_url(url_min_page_code, url_max_page_code)
    for url_item in all_the_urls:
        web_page_text = get_web_page(url_item)
        classify_article = get_article(web_page_text)
        if not classify_article:
            continue
        writer.writerow(classify_article)



store_in_csv('raw_news_data.csv')
