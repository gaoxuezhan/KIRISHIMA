import scrapy
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import scrapy
from lxml import etree, html
from shabbyRadar.items import ShabbyradarItem

import pandas as pd
import datetime
import pymysql

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class JdSpider(scrapy.Spider):
    name = "arleighBurke"
    # 打开数据库连接
    db = pymysql.connect(host='192.168.1.3', port=3307, user='gaoxz', passwd='gaoxz', db='KIRISHIMA', charset="utf8")
    filter = []
    dataRepository = []
    tableName = "MonetaryFund"

    def __init__(self):
        #关闭时通知清理战场，非常重要
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.get_filter()

    def spider_closed(self, spider):
        self.insert_by_many()
        self.db.close()
        # 关闭数据库连接
        print("清理战场！")

    def start_requests(self):
        for num in range(0, 1825):
            today = datetime.date.today()
            yesterday = today - datetime.timedelta(days=(num))
            output_yesterday = yesterday.strftime('%Y%m%d')

            url = 'http://data.chinafund.cn/hb/' + output_yesterday + '.html'

            if str(yesterday) not in self.filter:
                yield scrapy.Request(url, callback=self.parse,
                                     meta={"targetDate": yesterday.strftime('%Y-%m-%d'),
                                           'dont_redirect': True,
                                           'handle_httpstatus_list': [301, 302],
                                           'originURL': url},
                                            dont_filter=True)

    def parse(self, response):

        # ouput -> All
        soup = BeautifulSoup(response.body, from_encoding="utf-8")

        # ouput -> attrs={"ui-view": "content"}
        soup = BeautifulSoup(str(soup.select("#tablesorter > tbody")))

        targetDate = response.meta["targetDate"]

        report = soup.getText()
        # print(report)

        if response.url != response.meta['originURL']:
            url = 'http://data.chinafund.cn/hb/' + targetDate.replace("-", "") + '.html'
            print("命令已被窜改！302！ #对象日期->" + targetDate)
            yield scrapy.Request(url, callback=self.parse,
                                 meta={"targetDate": targetDate,
                                       'dont_redirect': True,
                                       'handle_httpstatus_list': [301, 302],
                                       'originURL': url},
                                 dont_filter=True)
        elif len(report) < 5:
            url = 'http://data.chinafund.cn/hb/' + targetDate.replace("-", "") + '.html'
            print("这他妈也交差！妈的，枪毙！滚回去重新搜索！ #对象日期->" + targetDate)
            yield scrapy.Request(url, callback=self.parse,
                                 meta={"targetDate": targetDate,
                                       'dont_redirect': True,
                                       'handle_httpstatus_list': [301, 302],
                                       'originURL': url},
                                 dont_filter=True)
        elif "对不起，没有该日数据！" in report:
            print("Sector Clear！ #对象日期->" + targetDate)
        else:
            print("Mission Complete！ #对象日期->" + targetDate)
            for tr in soup.findAll("tr"):
                item = ShabbyradarItem()
                item['date'] = targetDate
                item['id'] = tr.findAll("td")[0].string
                item['name'] = tr.findAll("td")[1].string
                item['value1'] = tr.findAll("td")[2].string
                item['value2'] = tr.findAll("td")[3].string
                yield item

    def output(self, filename, content):
        with open(filename, 'wb') as f:
            f.write(content)
        self.log('Saved file %s' % filename)

    def get_filter(self):
        with open('filter.txt', 'r') as f:
            for v in f.readlines():
                v = v.replace('\n', '')
                self.filter.append(v)

    # 批量插入executemany------------------------------------------------------------------------------------
    def insert_by_many(self):
        cursor = self.db.cursor()

        try:
            sql = "INSERT INTO " + "MonetaryFund" + " VALUES (%s, %s, %s, %s, %s)"
            # 批量插入
            cursor.executemany(sql, self.dataRepository)
            self.db.commit()
            print("--------------------------------------------快速存储成功！")
        except Exception as e:
            print("--------------------------------------------快速存储失败。。。")
            print(e)
            self.db.rollback()

            for v in self.dataRepository:
                self.insert_by_one(v)

        self.dataRepository.clear()

    def insert_by_one(self, item):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()

        # SQL 插入语句
        sql = "INSERT INTO " + "MonetaryFund" + " \
               VALUES (%s, %s, %s, %s, %s)" % \
              (item[0],
               item[1],
               item[2],
               item[3],
               item[4])
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except Exception as e:
            # 如果发生错误则回滚
            print(e)
            self.db.rollback()
        return item



