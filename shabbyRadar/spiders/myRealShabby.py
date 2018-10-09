import scrapy
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import scrapy
from lxml import etree, html


class JdSpider(scrapy.Spider):
    name = "kongou"
    # allowed_domains = ["jd.com"]
    start_urls = (
        # 'http://192.168.119.176/gt/device/index.html#/list',
        # 'http://192.168.119.176/gt/users/index.html#/user'
        'http://fund.cmbchina.com/FundPages/OpenFund/FundNetValue.aspx?Channel=OpenFund',
    )

    scripts = {}

    def __init__(self):
        self.driver = webdriver.Chrome("D:/NMCC/myNavy/AegisCombatSystem/chromedriver_win32/chromedriver.exe")
        self.scripts.clear

    def parse(self, response):
        url = response.url
        url = url.replace("://", "@@@")
        url = url.replace(".", "_")
        url = url.replace("/", "#")
        url = url.replace("?", "#")

        # ouput -> All
        soup = BeautifulSoup(response.body, from_encoding="utf-8")
        filename = 'D:/temp/%s' % url + "_All.html"
        self.output(filename, soup.prettify(encoding="utf-8"))

        # ouput -> attrs={"ui-view": "content"}
        soup = BeautifulSoup(str(soup.find("table")))
        filename = 'D:/temp/%s' % url + "_Content.html"
        self.output(filename, soup.prettify(encoding="utf-8"))

        result = ""
        temp = ""
        trs = soup.findAll("tr")
        for tr in trs:
            temp = ""
            for td in tr.findAll("td"):
                for x in td.strings:
                    x = x.strip()
                    x = x.strip('\n')
                    if len(x) > 0:
                        print(td.NavigableString)
                        print(td.string)
                        temp = temp + "," + x
            temp = temp[1:]
            result = result + temp + "\n"

        filename = 'D:/temp/%s' % url + "_String.html"
        self.output(filename, str(result).encode("utf-8"))
        #
        # # ouput -> buttons
        # soup = BeautifulSoup(str(soup.findAll("button")))
        # filename = 'D:/temp/%s' % temp + "_Buttons.html"
        # self.output(filename, soup.prettify(encoding="utf-8"))
        #
        # # click every button
        # buttons = soup.findAll("button")
        # for button in buttons:
        #     self.scripts.clear()
        #
        #     print(button['id'])
        #
        #     self.scripts[button['id']] = "click"
        #     yield scrapy.Request(response.url, callback=self.parse_click_button)

    def parse_click_button(self, response):

        temp = response.url
        temp = temp.replace("://", "@@@")
        temp = temp.replace(".", "_")
        temp = temp.replace("/", "#")
        temp = temp.replace("?", "#")

        # output -> All
        soup = BeautifulSoup(response.body, from_encoding="utf-8")

        for key in self.scripts.keys():
            temp = temp + "_" + key

        filename = 'D:/temp/%s' % temp + ".html"
        self.output(filename, soup.prettify(encoding="utf-8"))

    def output(self, filename, content):
        with open(filename, 'wb') as f:
            f.write(content)
        self.log('Saved file %s' % filename)


