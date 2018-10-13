import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from demo.config import *
from urllib.parse import quote

import time

# browser = webdriver.Chrome()
# browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)

wait = WebDriverWait(browser, 10)
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def index_page():
    """
    抓取索引页
    :param page: 页码
    """
    print('Take off!')
    try:
        url = 'https://login.taobao.com/member/login.jhtml'
        browser.get(url)

        time.sleep(10)

        url = 'https://sjipiao.fliggy.com/flight_search_result.htm?depDate=2018-11-03'
        browser.get(url)
        # from
        input1 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_NeSearch > div:nth-child(4) > label:nth-child(1) > input.pi-input.J_DepCity.ks-autocomplete-input')))
        # to
        input2 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_NeSearch > div:nth-child(4) > label:nth-child(2) > input.pi-input.J_ArrCity.ks-autocomplete-input')))
        # date
        # input3 = wait.until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, '#J_NeSearch > div:nth-child(5) > label:nth-child(1) > div > input')))

        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_NeSearch > span > span > input')))

        input1.clear()
        input2.clear()
        # input3.clear()
        input1.send_keys('北京')
        input2.send_keys('深圳')
        # input3.send_keys('2018')
        # input3.send_keys('-')
        # input3.send_keys('11')
        # input3.send_keys('-')
        # input3.send_keys('02')

        submit.click()

        # wait.until(
        #     EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_FlightListBox > div:nth-child(1) > table > tbody > tr')))
        get_products()
    except TimeoutException:
        index_page()

def get_products():
    """
    提取商品数据
    """
    html = browser.page_source
    print(html)
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)


def save_to_mongo(result):
    """
    保存至MongoDB
    :param result: 结果
    """
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')


def main():
    """
    遍历每一页
    """
    index_page()
    browser.close()


if __name__ == '__main__':
    main()