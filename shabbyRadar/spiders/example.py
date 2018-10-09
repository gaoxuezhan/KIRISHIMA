import re
import scrapy                                   #导入scrapy包
from bs4 import BeautifulSoup
from scrapy.http import Request                 ##一个单独的request的模块，需要跟进URL的时候，需要用它
from shabbyRadar.items import ShabbyradarItem   ##这是我定义的需要保存的字段，（导入dingdian项目中，items文件中的DingdianItem类）

class Myspider(scrapy.Spider):

    name = 'dingdian'
    # allowed_domains = ['23wx.cc']
    bash_url = 'http://www.23wx.cc/class/'
    bashurl = '.html'

    def start_requests(self):
        for i in range(1, 11):
            url = self.bash_url + str(i) + '_1' + self.bashurl
            yield Request(url, self.parse)
        # yield Request('http://www.23wx.com/quanben/1', self.parse)

    def parse(self, response):
        filename = response.url + '.html'
        filename = filename.replace("/", "")
        filename = filename.replace(".", "")
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
