# *-* coding:utf-8 *-*  
import requests
from bs4 import BeautifulSoup
import lxml
from multiprocessing import Process, Queue
import random
import json
import time
import requests


class Proxies(object):
    """docstring for Proxies"""

    def __init__(self, page=3):
        self.proxies = []
        self.verify_pro = []
        self.page = page
        self.headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        self.get_proxies()
        self.get_proxies_nn()

    def get_proxies(self):
        # page = random.randint(1, 10)
        # page_stop = page + self.page
        # while page < page_stop + 30:
        #     url = 'http://www.xicidaili.com/wt/%d' % page
        #     html = requests.get(url, headers=self.headers).content
        #     soup = BeautifulSoup(html, 'lxml')
        #     ip_list = soup.find(id='ip_list')
        #     for odd in ip_list.find_all(class_='odd'):
        #         protocol = odd.find_all('td')[5].get_text().lower() + '://'
        #         if "s" not in protocol:
        #             self.proxies.append(protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
        #     page += 1
        pass

    def get_proxies_nn(self):
        '''随机从文件中读取proxy'''
        while 1:
            with open('D:\\NMCC\\myNavy\\AegisCombatSystem\\KIRISHIMA\\proxies_prepare.txt', 'r') as f:
                proxies = f.readlines()
            if proxies:
                break
            else:
                time.sleep(1)

        for v in proxies:
            v = v.replace('\n', '')
            self.proxies.append(v)

    def verify_proxies(self):
        # 没验证的代理
        old_queue = Queue()
        # 验证后的代理
        new_queue = Queue()
        print('verify proxy........')
        works = []
        for _ in range(15):
            works.append(Process(target=self.verify_one_proxy, args=(old_queue, new_queue)))
        for work in works:
            work.start()
        for proxy in self.proxies:
            old_queue.put(proxy)
        for work in works:
            old_queue.put(0)
        for work in works:
            work.join()
        self.proxies = []
        while 1:
            try:
                self.proxies.append(new_queue.get(timeout=1))
            except:
                break
        print('verify_proxies done!')

    def verify_one_proxy(self, old_queue, new_queue):
        while 1:
            proxy = old_queue.get()
            if proxy == 0: break
            protocol = 'https' if 'https' in proxy else 'http'
            proxies = {protocol: proxy}
            try:
                # if requests.get('http://www.baidu.com', proxies=proxies, timeout=5).status_code == 200:
                if requests.get('http://data.chinafund.cn/hb/20170605.html', proxies=proxies, timeout=5).status_code == 200:
                    print('success %s' % proxy)
                    new_queue.put(proxy)
                    with open('proxies.txt', 'a') as f:
                        f.write(proxy + '\n')
            except:
                print('fail %s' % proxy)


if __name__ == '__main__':
    a = Proxies()
    a.verify_proxies()
    print(a.proxies)
    proxie = a.proxies
    # with open('proxies.txt', 'a') as f:
    #     for proxy in proxie:
    #         f.write(proxy + '\n')