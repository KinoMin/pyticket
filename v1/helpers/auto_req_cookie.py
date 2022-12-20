

import random
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import v1.helpers.req
from v1.helpers import req
from v1.helpers.api import *
from v1.helpers.parameter import *
from v1.helpers.api import MY_12306


class Cookie(object):

    def getCookie(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation']) # 打开驱动参数
        # options.add_experimental_option('prefs', {'profile.default_co、ntent_setting_values': {'images': 2}}) # 无图片
        for argument in reptile_argument:
            options.add_argument(argument)

        browser = webdriver.Chrome(options=options)
        # browser.implicitly_wait(10) # 隐式等待
        wait = WebDriverWait(browser, 10)  # 显示等待
        browser.get(API_BASE_LOGIN.get('url'))
        browser.maximize_window()
        wait.until(EC.visibility_of_element_located((By.ID, 'J-userName'))).send_keys(LOGIN_USERNAME)
        wait.until(EC.visibility_of_element_located((By.ID, 'J-password'))).send_keys(LOGIN_PASSWORD)
        wait.until(EC.visibility_of_element_located((By.ID, 'J-login'))).click()
        sleep(2)

        action_chains = ActionChains(browser)
        action_chains.drag_and_drop_by_offset(browser.find_element(By.ID, 'nc_1_n1z'), 600, 0).perform()
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'ok'))).click() # 关闭弹出框
        wait.until(EC.visibility_of_element_located((By.ID, 'houbudingdan'))).click() # 按 候补订单 按钮
        action_chains.move_to_element(browser.find_element(By.ID, 'J-chepiao')).click().perform()
        action_chains.move_to_element(browser.find_element(By.XPATH, '//*[@id="megamenu-3"]/div[1]/ul/li[1]/a')).click().perform()
        wait.until(EC.visibility_of_element_located((By.ID, 'fromStationText'))).click()
        wait.until(EC.visibility_of_element_located((By.ID, 'fromStationText'))).send_keys('shenzhenbei')
        wait.until(EC.visibility_of_element_located((By.ID, 'fromStationText'))).send_keys(Keys.ENTER)
        wait.until(EC.visibility_of_element_located((By.ID, 'toStationText'))).click()
        wait.until(EC.visibility_of_element_located((By.ID, 'toStationText'))).send_keys('wuhan')
        wait.until(EC.visibility_of_element_located((By.ID, 'toStationText'))).send_keys(Keys.ENTER)
        wait.until(EC.visibility_of_element_located((By.ID, 'query_ticket'))).click()  # 查询
        cookies = browser.get_cookies()

        cookie = [item['name'] + '=' + item['value'] for item in cookies]
        cookie = '; '.join(item for item in cookie)
        with open('/Users/kino/works/kino/quick-deploy/ticket/v1/tmp/cookie.txt', 'w') as f:
            f.write(cookie)
            v1.helpers.req.headers['Cookie'] = cookie

    def invalid(self):
        try:
            while True:
                cookie = ''
                with open('/Users/kino/works/kino/quick-deploy/ticket/v1/tmp/cookie.txt', 'r') as f:
                    cookie = f.readline()
                ## 校验 cookie 是否失活
                req.headers['Referer'] = 'https://kyfw.12306.cn/otn/view/index.html'
                req.headers['Cookie'] = cookie
                response = requests.post(url=MY_12306.get('url'), headers=req.headers, proxies=req.proxies)
                if response.status_code == 200 and 'DOCTYPE' not in response.text:
                    print('cookie 有效')
                    v1.helpers.req.headers['Cookie'] = cookie
                    break
                else:
                    print('cookie 失效，开始重新获取')
                    self.getCookie()
        except Exception as e:
            print('获取 cookie 失败: %s ' % str(e))

# Cookie().invalid()