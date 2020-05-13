# 爬取豆瓣top250所有页面的数据, 如果被识别为爬虫没关系，利用代理IP
import requests
from lxml import etree
import time

# 免费代理一般质量不高，容易造成请求响应超时，建议自行购买IP代理
# proxies = {'http': 'http://112.87.70.91:9999', 'https': 'http://1112.87.70.91:9999'}
# 解决办法：模拟登陆也可解决


# 创建爬取数据豆瓣类
class DoubanSpider(object):
    """
    1. 初始化要爬取的url, 头信息headers
    2. 向网页发送get请求， 这里用的是requests库
    3. 解析获取的html页面，获取所有的详情页url
    """
    def __init__(self, urls, headers):
        self.urls = urls
        self.headers = headers

    # 获取所有电影详情页
    def detail_url(self, url):
        try:
            response = requests.get(url=url, headers=self.headers)  # 模拟网页，发送get请求
        except Exception as e:  # 处理异常
            print(e)
            return 0
        detail_urls = []
        # print(response.status_code)
        if response.status_code == 200:  # 判断请求是否为200状态码， 否侧请求会报异常或403
            html = response.text  # 抓取网页html
            text = etree.HTML(html)
            lis = text.xpath("//div[@class='article']//li")  # 利用xpath来获取所有元素li标签

            for li in lis:
                page_detail_url = li.xpath(".//div[@class='pic']/a/@href")[0]
                self.parse_detail_page(page_detail_url)
                detail_urls.append(page_detail_url)
        return detail_urls  # 这里返回值获取不到，还没发现问题，等会我看看(已解决)

    # 开始解析详情页数据
    def parse_detail_page(self, detail_url):
        response = requests.get(url=detail_url, headers=self.headers)  # 发送详情页get请求
        html = response.text

        text = etree.HTML(html)
        movie_name = text.xpath("//div[@id='content']//h1/span/text()")[0]  # 获取电影名称
        describe = text.xpath("//div[@id='link-report']/span/text()")  # 获取电影描述信息
        # 处理描述信息
        # describe = ''.join(describe).replace('\n', '').strip()  # 去除列表，和前后空格
        describe = ''.join(describe).replace('\n', '')  # 去除列表，和前后空格
        print("电影：《{}》".format(movie_name))
        print("描述信息：")
        print(describe + '\n')

    def run(self):
        page_num = 1
        for u in self.urls:
            print("开始爬取" + str(page_num) + "页数据")
            url = u
            self.detail_url(url)
            page_num += 1
            time.sleep(3)


if __name__ == '__main__':
    page_url = "https://movie.douban.com/top250?start={}"  # 要爬取的指定网页,依次是0， 25， 50， ...
    HEADERS = {  # 请求头信息，防止被识别为爬虫
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/75.0.3770.100 Safari/537.36",
            "Referer": "https://accounts.douban.com/passport/login?redir=https%3A%2F%2Fmovie.douban.com%2Ftop250",
            "Cookie": 'bid=WksF6FR0EwE; douban-fav-remind=1; ll="118190"; __'
                      'yadk_uid=f2QUAF6pZxhOkBknVaaJqoSNbhPKfo8k; _'
                      'vwo_uuid_v2=D6EC58A760CCF42055BED40BFAE29D6A2|c11e1491d9a0ab6399a6f5389472750b; _'
                      '_gads=ID=ef2109ee773e775e:T=1581425287:S=ALNI_MZm6S4YI3_oZ98A1uJaIZGTDIfHqg; _'
                      '_utmv=30149280.21269; '
                      '_ga=GA1.2.2000237357.1563892310; douban-profile-remind=1; viewed="4212921";'
                      ' gr_user_id=f4a4f0ad-747d-464f-bed0-fb4fb9fbea74; __utmc=30149280; _'
                      '_utmz=30149280.1589027476.20.15.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _'
                      '_utmc=223695111; __utmz=223695111.1589027476.13.9.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; '
                      'ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1589035460%2C%22https%3A%2F%2F'
                      'www.baidu.com%2Flink%3Furl%3DdHAoIOR-wsSesFAJCP8c-ailQOXOhQAAiqRDn-RC5ObNGgkroQishnFNfMkeW_'
                      'GK%26wd%3D%26eqid%3Dbef3b5de00014633000000055eb6a1b4%22%5D; _pk_ses.100001.4cf6=*; '
                      'utma=30149280.2000237357.1563892310.1589027476.1589035460.21; __utmb=30149280.0.10.1589035460; '
                      '__utma=223695111.1683471889.1581425357.1589027476.1589035460.14;'
                      '__utmb=223695111.0.10.1589035460; dbcl2="212690861:uOETaPF32Lw"; ck=91Ua; '
                      '_pk_id.100001.4cf6=d76186e142e4ab46.1581425358.14.1589036208.1589033498.;'
                      ' push_noty_num=0; push_doumail_num=0'
    }
    page_urls = []
    for i in range(0, 10):
        page = page_url.format(i*25)  # 0-225
        page_urls.append(page)
    douban_spider = DoubanSpider(urls=page_urls, headers=HEADERS)
    douban_spider.run()
