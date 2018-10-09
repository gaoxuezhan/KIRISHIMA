import scrapy
from selenium import webdriver

import scrapy


class JdSpider(scrapy.Spider):
    name = "jd"
    # allowed_domains = ["jd.com"]
    start_urls = (
        'http://search.jd.com/Search?keyword=amd&enc=utf-8',
        'http://192.168.119.176/gt/login/index.html#'
    )

    def parse(self, response):
        print(response.body)
