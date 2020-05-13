# 最简单的爬虫（利用requests爬取豆瓣top250电影信息）

# 1 导包（这里用到的主要有requests）
import requests
from lxml import etree
import json

# 2 确认要抓取的网址 https://movie.douban.com/top250

url = "https://movie.douban.com/top250"

# 3 头信息设置，这个是关键，防止被识别为爬虫，但不一定肯定能避免被识别，当处理反爬虫网站时，需要通过IP代理池来进行爬取数据

headers = {
    # 头信息在网页上可以直接复制，F12找到网页地址，直接拷贝
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/75.0.3770.100 Safari/537.36"

}


response = requests.get(url=url, headers=headers)

html = response.text  # 获取网页，接下里我们开始拿数据， 这里我们需要利用xpath

text = etree.HTML(html)  # <Element html at 0x4116440> 网页元素对象

# 4. 分析网页，准备拿取数据， 我们先拿取一个最简单的试试
title = text.xpath("//div[@id='content']/h1/text()")[0]  # 很简单的拿到标题数据

# 现在开始拿取第一页所有的数据
lis = text.xpath("//div[@class='article']//li")  # 拿到所有的li标签

# 这里定义列表用来存储电影拿取的字段
movies_li = []


# for循环遍历所有li标签
for li in lis:
    movies_dic = {}
    movie_name = li.xpath(".//div[@class='info']"
                          "/div[@class='hd']/a/span/text()")[0]  # 拿取所有电影名称（第一页）

    detail_url = li.xpath(".//div[@class='item']/div[@class='pic']//a/@href")[0]  # 拿取所有电影详情url
    image_url = li.xpath(".//div[@class='item']/div[@class='pic']//a/img/@src")[0]  # 拿取所有电影图片url

    movies_dic["movie_name"] = movie_name
    movies_dic["image_url"] = image_url  # 太蠢了。。。。
    movies_dic["detail_url"] = detail_url
    print(movies_dic)
    movies_li.append(movies_dic)









