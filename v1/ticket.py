# -*- coding:utf-8 -*-

"""
12306 抢票
"""

import threading
import schedule
from v1.buy.ticket_buy import *
from v1.helpers.auto_req_cookie import Cookie
from v1.model.entity import InputInfo

def Main():
    print('\n\nstart buy ticket...')
    try:
        passengers = '宋朋'
        from_time = '2022-12-21'
        from_input = '深圳北'
        to_input = '武汉'
        seat_type = '二等座'
        train_number = 'G1002'
        scope_time = '08-24'
        ifo = InputInfo(passengers=passengers, from_time=from_time, from_input=from_input, to_input=to_input, seat_type=seat_type, train_number=train_number, scope_time=scope_time)

        tickets = ticketBuy().query_ticket(inputinfo=ifo)  ## 余票
        secretStr, train = ticketBuy().check_train_number(trains=tickets, inputinfo=ifo)  ## 预约车次
        token = ticketBuy().initDc()  ## 获取 token
        userinfo = ticketBuy().getUserInfo(token=token, inputinfo=ifo) ## 获取乘客信息
        ticketBuy().checkOrderInfo(userinfo=userinfo, token=token)  ## 检查订单状态
        ticketBuy().getQueueCount(token=token, train=train)  ## 查询队列
        # ticketBuy().submitOrder(token=token, userinfo=userinfo, train=train)  ## 提交订单
        info_dict = ticketBuy().queryMyOrderNoComplete()  ## 查询待支付订单
        print(info_dict)
        print('抢票成功，请及时支付')
    except Exception as e:
        print('兄弟, 程序噶了, %s ' % str(e))

def start():
    invalid = threading.Timer(interval=3, function=schedule.every(3).seconds.do(Cookie().invalid))
    # update = threading.Timer(interval=120, function=schedule.every(2).minutes.do(Cookie().getCookie))
    # buy = threading.Timer(interval=3, function=schedule.every(10).seconds.do(Main))
    # schedule.every(3).seconds.do(Cookie().invalid)  # 每 3 秒执行一次校验 cookie
    # schedule.every(2).minutes.do(Cookie().getCookie)  # 每 2 分钟执行一次强制更新 cookie
    # schedule.every(10).seconds.do(Main)   # 每10秒执行一次
    invalid.start()
    # update.start()
    # buy.start()

    while True:
        schedule.run_pending()
        time.sleep(2)

start()