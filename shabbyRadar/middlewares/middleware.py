from scrapy.http import HtmlResponse
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class JavaScriptMiddleware(object):
    def process_request(self, request, spider):

        # Chrome------------------------------------------------------------------------------------------------
        options = webdriver.ChromeOptions()
        # 1允许所有图片；2阻止所有图片；3阻止第三方服务器图片
        # 禁用js
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2,
                'javascript': 2
            }
        }
        options.add_experimental_option('prefs', prefs)
        if "proxy" in request.meta:
            options.add_argument('--proxy-server={0}'.format(request.meta['proxy'].replace("http://", "")))

        driver = webdriver.Chrome(
            executable_path="D:/NMCC/myNavy/AegisCombatSystem/chromedriver_win32/chromedriver.exe",
            chrome_options=options)


        # Phantomjs------------------------------------------------------------------------------------------------
        #
        # phantomjs_driver_path = "D:/NMCC/myNavy/AegisCombatSystem/phantomjs-2.1.1-windows/phantomjs.exe"
        #
        # dcap = dict(DesiredCapabilities.PHANTOMJS)
        # # # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
        # # dcap["phantomjs.page.settings.userAgent"] = (random.choice(USER_AGENTS))
        # # 不载入图片，爬页面速度会快很多
        # dcap["phantomjs.page.settings.loadImages"] = False
        # # # 设置代理
        # if "proxy" in request.meta:
        #     temp = "--proxy=" + request.meta['proxy'].replace("http://", "")
        #     service_args = [temp, '--proxy-type=http', '--ignore-ssl-errors=true', '--ssl-protocol=TLSv1']
        # else:
        #     service_args = []
        #
        #
        # # 打开带配置信息的phantomJS浏览器
        # driver = webdriver.PhantomJS(phantomjs_driver_path, desired_capabilities=dcap, service_args=service_args)
        # # 隐式等待5秒，可以自己调节
        # driver.implicitly_wait(5)
        # # # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
        # # # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
        # # driver.set_page_load_timeout(10)
        # # 设置10秒脚本超时时间
        # driver.set_script_timeout(1)
        #
        # driver.get('http://1212.ip138.com/ic.asp')
        # print(driver.page_source)
        #
        # ------------------------------------------------------------------------------------

        # driver = webdriver.PhantomJS()

        # # try to use the proxy
        # # 现在开始切换ip
        # # 再新建一个ip
        # proxy = Proxy(
        #     {
        #         'proxyType': ProxyType.MANUAL,
        #         # 'httpProxy': 'ip:port'  # 代理ip和端口
        #         'httpProxy': request.meta['proxy'].replace("http://", "")
        #     }
        # )
        # # 再新建一个“期望技能”，（）
        # desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        # # 把代理ip加入到技能中
        # proxy.add_to_capabilities(desired_capabilities)
        # # 新建一个会话，并把技能传入
        # spider.driver.start_session(desired_capabilities)
        # spider.driver.get('http://httpbin.org/ip')
        # print(spider.driver.page_source)

        # # 利用DesiredCapabilities(代理设置)参数值，重新打开一个sessionId，我看意思就相当于浏览器清空缓存后，加上代理重新访问一次url
        # proxy = webdriver.Proxy()
        # proxy.proxy_type = ProxyType.MANUAL
        # proxy.http_proxy = request.meta['proxy'].replace("http://", "")
        # # 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中
        # proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
        # driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
        driver.get('http://1212.ip138.com/ic.asp')
        print(driver.page_source)

        targeturl = request.url
        driver.get(targeturl)

        driver.implicitly_wait(5)

        # # 显式等待
        # try:
        #     element = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.ID, "tablesorter"))
        #     )
        # finally:
        #     # driver.close()
        #     pass

        if "login" in driver.current_url:
            driver.find_element_by_id("enterpriseName").clear()
            driver.find_element_by_id("enterpriseName").send_keys("enterprise123")
            driver.find_element_by_id("enterpriseGroupName").clear()
            driver.find_element_by_id("enterpriseGroupName").send_keys("enterpriseGroup321")
            driver.find_element_by_id("userid").clear()
            driver.find_element_by_id("userid").send_keys("linyouxi")
            driver.find_element_by_id("password").clear()
            driver.find_element_by_id("password").send_keys("Bhh-hit2017")
            driver.find_element_by_id("loginButton").click()
            driver.implicitly_wait(5)
            driver.get(targeturl)
            driver.implicitly_wait(5)

        # time.sleep(2)

        # driver.find_element_by_id("jqg_grid1_1").click()
        time.sleep(1)

        if "scenarioes" in request.meta:
            myMeta = request.meta["scenarioes"]
            print(myMeta)

            for key, value in myMeta:
                if "scenario-click" in key:
                    button = driver.find_element_by_css_selector(value)
                    button.click()
                    time.sleep(1)
                if "scenario-input" in key:
                    css_selector = value.split("#@#")[0]
                    input_value = value.split("#@#")[1]
                    tag = driver.find_element_by_css_selector(css_selector)
                    tag.clear()
                    tag.send_keys(input_value)
                    time.sleep(1)

        # print(request.meta)

        driver.implicitly_wait(5)
        js = "var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js) #可执行js，模仿用户操作。此处为将页面拉至最底端。
        driver.implicitly_wait(5)
        body = driver.page_source
        url = driver.current_url

        driver.quit()

        return HtmlResponse(url, body=body, encoding='utf-8', request=request)
