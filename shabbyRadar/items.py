# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShabbyradarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 净值日期
    date = scrapy.Field()
    # 基金代码
    id = scrapy.Field()
    # 基金简称
    name = scrapy.Field()
    # 单位净值(元)
    value1 = scrapy.Field()
    # 累计净值(元)
    value2 = scrapy.Field()

