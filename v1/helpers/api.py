# coding=utf-8

HOST_URL = 'kyfw.12306.cn'
BASE_URL = 'https://' + HOST_URL

API_BASE_LOGIN = {
    'url': BASE_URL + '/otn/resources/login.html'
}

## 验证登录
UMATK_URL = {
    'url': BASE_URL + 'passport/web/auth/uamtk-static'
}

## 我的首页
MY_12306 = {
    'url': BASE_URL + '/otn/index/initMy12306Api'
}

QUERY_URL = {
    'url': BASE_URL + '/otn/leftTicket/query'
}

REFERER_URL = {
    'url': BASE_URL + '/otn/leftTicket/init'
}

SUBMIT_URL = {
    'url': BASE_URL + '/otn/leftTicket/submitOrderRequest'
}

INIT_DC = {
    'url': BASE_URL + '/otn/confirmPassenger/initDc'
}

GET_PASSENGER_URL = {
    'url': BASE_URL + '/otn/confirmPassenger/getPassengerDTOs'
}

CHECK_ORDER_INFO = {
    'url': BASE_URL + '/otn/confirmPassenger/checkOrderInfo'
}

GET_QUEUE_COUNT = {
    'url': BASE_URL + '/otn/confirmPassenger/getQueueCount'
}

SUBMIT_ORDER = {
    'url': BASE_URL + '/otn/confirmPassenger/confirmSingleForQueue'
}

QUERY_MY_ORDER = {
    'url': BASE_URL + '/otn/queryOrder/queryMyOrderNoComplete'
}