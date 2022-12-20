""" 校验 cookie 是否失效 """

import requests
from v1.helpers.auto_req_cookie import Cookie

class invalid_cookie(object):

    def __init__(self):
        self.cookie = Cookie().read_cookie(filepath='../tmp/cookie.txt')

    def invalid(self, tmp):
        url1  = 'https://kyfw.12306.cn/otn/index/initMy12306Api'
        url2 = 'https://kyfw.12306.cn/otn/modifyUser/initQueryUserInfoApi'
        url3 = 'https://kyfw.12306.cn/otn/passengers/query'
        data2 = {
            'pageIndex': '1',
            'pageSize': '10'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'Cookie': self.cookie
        }
        response1 = requests.post(url1, cookies=self.cookie, headers=headers).text
        response2 = requests.post(url2, cookies=self.cookie, headers=headers).text
        response3 = requests.post(url3, cookies=self.cookie, data=data2, headers=headers).text
        if '_validatorMessage' in response1 and '_validatorMessage' in response2 and '_validatorMessage' in response3:
            print(response1)
            print(response2)
            print(response3)
            print("服务器登录验证成功")
            return True
        else:
            print('服务器登录验证失败')
            return False

        # query_order_url = 'https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete'
        # data = {
        #     '_json_att': ''
        # }
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        #     'Cookie': self.cookie
        # }
        # response = requests.post(url=query_order_url, data=data, headers=headers)
        # print(response.text)

invalid_cookie().invalid(tmp='1')