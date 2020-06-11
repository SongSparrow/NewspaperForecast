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
file_name = ""

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


def get():
    for i in range(url_min_page_code, url_max_page_code + 1):
        url_realistic = url_head + str(i) + '-1.html'
        # 获取对应url的html文档
        response = rq.get(url_realistic, headers=_headers)
        if not_exist(response.text):
            return None

        document = pq(response.text)
        # 检测日期
        date_text = document(".ibox span").text()
        date_str = date_text.split(":")
        date = date_str[1].strip()
        if not_within_date(date):
            return None

        # 获取文件名称

        # 获取文章的正文内容

        # 存储文章



