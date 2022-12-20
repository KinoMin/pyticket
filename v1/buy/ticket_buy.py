"""
购票主类
"""

# 引入依赖
import re
import time
import requests
import json
from datetime import datetime

# 自定义
from v1._utils.Station import Station
from v1._utils.Variable import Variable
from v1._utils.encoding import encoding
from v1.helpers import req
from v1.helpers.api import *
from v1.model.entity import Train


class ticketBuy(object):

    def weekdays(self, apply_time):
        apply_week = datetime.strptime(apply_time, "%Y-%m-%d").weekday() + 1
        return str(apply_week)

    """ 查询余票 """
    def query_ticket(self, inputinfo):
        result_json = []
        try:
            print('########################## 查询余票 ##########################')
            station = Station()
            data = {
                'leftTicketDTO.train_date': inputinfo.from_time,
                'leftTicketDTO.from_station': station.getStationForValue(inputinfo.from_input),
                'leftTicketDTO.to_station': station.getStationForValue(inputinfo.to_input),
                'purpose_codes': 'ADULT'
            }
            req.headers['Referer'] = REFERER_URL.get('url')
            response = requests.get(url=QUERY_URL.get('url'), params=data, headers=req.headers, proxies=req.proxies)
            response.encoding = encoding(response)
            j_result = json.loads(response.text)
            results = j_result['data']['result']
            if len(results) > 0:
                for result in results:
                    record = str(result).split('|')
                    if record[0] != '':
                        current_data = time.strftime('%Y-%m-%d', time.localtime())
                        result_json.append(
                            Train(
                                record[0],
                                record[13],
                                record[3],
                                record[31],
                                record[30],
                                str(datetime.strptime(current_data + ' ' + record[8], '%Y-%m-%d %H:%M')),
                                str(datetime.strptime(current_data + ' ' + record[9], '%Y-%m-%d %H:%M')),
                                station.getStation(key=record[6]),
                                station.getStation(key=record[7]),
                                record[2],
                                record[15]
                            )
                        )
            else:
                raise Exception('暂无余票')
        except json.decoder.JSONDecodeError as e:
            raise json.decoder.JSONDecodeError('ip 被限制, 错误信息: %s' % str(e))
        except Exception as e:
            raise Exception('查询余票出现未知错误, 错误信息: %s' % str(e))
        return result_json

    """ 预约(选择车次) """
    def check_train_number(self, trains, inputinfo):
        print('########################## 根据条件开始预约车次 ##########################')
        result_secret = ''
        result_train = None
        req.headers['Referer'] = REFERER_URL.get('url')
        try:
            for train in trains:
                if train.train_num == inputinfo.train_number:
                    result_train = train
                    sec = train.secret_str
                    result_secret = sec.replace('%2F', '/').replace('%0A', '').replace('%2B', '+').replace('%3D', '=')
                    data = {
                        'secretStr': '%s' % result_secret,
                        'train_date': '%s' % train.start_data,
                        'back_train_date': '%s' % train.end_date,
                        'tour_flag': 'dc',
                        'purpose_codes': 'ADULT',
                        'query_from_station_name': '%s' % train.from_station,
                        'query_to_station_name': '%s&undefined' % train.to_station
                    }
                    response = requests.post(url=SUBMIT_URL.get('url'), data=data, headers=req.headers, proxies=req.proxies)
                    if '200' in response.text:
                        print('开始预约车次为: %s 的车票' % train.train_num)
            if result_secret == '' or result_train is None:
                raise Exception('在 %s 这天没有车次为 %s 的列车' % (inputinfo.from_time, inputinfo.train_number))
        except Exception as e:
            raise Exception('预约车次出现位置错误, 错误信息: %s' % str(e))
        return result_secret, result_train

    def initDc(self):
        url = INIT_DC.get('url')
        data = {
            '_json_att': ''
        }
        req.headers['Referer'] = REFERER_URL.get('url')
        try:
            response = requests.post(url=url, data=data, headers=req.headers, proxies=req.proxies)
            globalRepeatSubmitToken = re.search(r"globalRepeatSubmitToken = '(.*?)'", response.text)
            leftTicket = re.search(r"'leftTicketStr':'(.*?)'", response.text)
            ticketInfoForPassengerForm = re.search(r"ticketInfoForPassengerForm=(.*?);", response.text)
        except Exception as e:
            raise Exception('查询 global token 失败, 错误信息: %s' % str(e))
        else:
            if globalRepeatSubmitToken is None or leftTicket is None or ticketInfoForPassengerForm is None:
                raise Exception('查询不到 global token')
        return globalRepeatSubmitToken, leftTicket, ticketInfoForPassengerForm

    """ 获取乘客信息 """
    def getUserInfo(self, token, inputinfo):
        print('########################## 获取该账号下的乘客信息 ##########################')
        get_url = GET_PASSENGER_URL.get('url')
        req.headers['Referer'] = REFERER_URL.get('url')
        data = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': token[0].group(1)
        }
        result_user_info = None
        try:
            response = requests.post(url=get_url, data=data, headers=req.headers, proxies=req.proxies)
            userinfo = json.loads(response.text)['data']['normal_passengers']
            for info in userinfo:
                if info['passenger_name'] == inputinfo.passengers:
                    result_user_info = info
                    print('购买用户: %s' % info['passenger_name'])
                    break
        except Exception as e:
            raise Exception('获取乘客信息失败, 错误信息: %s' % str(e))
        else:
            if result_user_info is None:
                raise Exception('该账号下没有 %s 乘客信息。' % inputinfo.passengers)
            else:
                return result_user_info

    """ 检查订单状态 """
    def checkOrderInfo(self, userinfo, token):
        print('########################## 开始检查订单状态 ##########################')
        check_url = CHECK_ORDER_INFO.get('url')
        req.headers['Referer'] = INIT_DC.get('url')
        data = {
            'cancel_flag': '2',
            'bed_level_order_num': '000000000000000000000000000000',
            'passengerTicketStr': 'O,0,1,{},1,{},{},N,{}'.format(userinfo['passenger_name'], userinfo['passenger_id_no'], userinfo['mobile_no'], userinfo['allEncStr']),
            'oldPassengerStr': '{},1,{},1_'.format(userinfo['passenger_name'], userinfo['passenger_id_no']),
            'tour_flag': 'dc',
            'randCode': '',
            'whatsSelect': '1',
            'sessionId': '',
            'sig': '',
            'scene': 'nc_login',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': token[0].group(1),
        }
        try:
            response = requests.post(url=check_url, data=data, headers=req.headers, proxies=req.proxies)
        except Exception as e:
            raise Exception('检查订单状态失败, 错误信息: %s' % str(e))
        else:
            if '200' in response.text:
                print('订单检查成功, 返回消息: ', response.text)

    def getQueueCount(self, token, train):
        print('########################## 查询该列车的余票和座位号 ##########################')
        station = Station()
        url = GET_QUEUE_COUNT.get('url')
        data = {
            'train_date': '{} {} {} {} 00:00:00 GMT+0800 (中国标准时间)'.format(
                Variable.xingqi[self.weekdays(Variable.date)],
                Variable.yuefen[Variable.date.split('-')[1]],
                Variable.date.split('-')[2],
                Variable.date.split('-')[0]),
            'train_no': train.train_no[0],
            'stationTrainCode': train.train_num,
            'seatType': '0',
            'fromStationTelecode': station.getStationForValue(value=train.from_station),
            'toStationTelecode': station.getStationForValue(value=train.to_station),
            'leftTicket': token[1].group(1),
            'purpose_codes': '00',
            'train_location': train.start_local,
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': token[0].group(1),
        }
        # req.headers['Referer'] = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
        try:
            response = requests.post(url=url, data=data, headers=req.headers, proxies=req.proxies)
        except Exception as e:
            raise Exception('查询列车: %s 的余票和座位号出现异常, 错误信息: %s' % (train.train_no[0], str(e)))
        else:
            if '200' in response.text:
                print('查询座位队列成功, 返回消息: %s' % response.text)
            else:
                print('查询座位队列失败, 返回消息: %s' % response.text)

    def submitOrder(self, token, userinfo, train):
        print('########################## 准备提交订单 ##########################')
        submit_url = SUBMIT_ORDER.get('url')
        req.headers['Referer'] = INIT_DC.get('url')
        data = {
            'passengerTicketStr': 'O,%s,%s,%s,%s,%s,%s,%s,%s' %
                                  (
                                      userinfo['index_id'],
                                      userinfo['passenger_type'],
                                      userinfo['passenger_name'],
                                      userinfo['passenger_id_type_code'],
                                      userinfo['passenger_id_no'],
                                      userinfo['mobile_no'],
                                      userinfo['is_buy_ticket'],
                                      userinfo['allEncStr']
                                  ),
            'oldPassengerStr': '%s,%s,%s,1_' % (userinfo['passenger_name'], userinfo['passenger_type'], userinfo['passenger_id_no']),
            'randCode': '',
            'purpose_codes': '00',
            'key_check_isChange': re.search(r"'key_check_isChange':'(.*?)'", token[2].group(1)).group(1),
            'leftTicketStr': token[1].group(1),
            'train_location': train.start_local,
            'choose_seats': '1F',
            'seatDetailType': '000',
            'is_jy': 'N',
            'is_cj': 'Y',
            'encryptedData': 'iXuJ1BXdNvcMwD2NAb9LwynD.4a6bh6nN63gUQFu_BsMCTzZgYlWIy.jYVEEbb5jdBNUh600lorZ9XZQGUVLzJBWMnU04kq3_Bj9zVSgLGRyovLWaJSaDPcJSMqaIISnyZylfUaaqzCE4DwHxZ6xXqcDXP4OYf_W3tQ1iLjJYlBMQf8GzcCpmKQU3m4RbYwjYK6iHTjL9RrxwwriOMMXCd03l6SzXBvUflExkptXFOGMvz3dV1ii2Qxda9EGC2sK9sVG1FuMogBdWwxcsO1MEadlHJSVXUjP8J5PIAxTtcTj4SSj4chtbLlmWOeKPeuitM4gBrYwdlNwk8qzU6Q4tMz2UupnS6edk84_qsGiUCAtvC0EFzgk84eGUMzdrRYzn4o0V6gZvMljbRR1W0lmXsjos89phpnQKnvGBpz3itjIsKdQXVLZdU7k30HBN5NB393pkCTGykM29O9FsYtcpXSHjm9YhY2s1wCFrTkscE5QNmuYf5trXNsqK6JksqUumPEFDyXnVekrJBVav9SNtuP_6KsLs3PmV1lWYhDdx4c8tYvTK3uzBMd3X5vj1SXz.Np.t0nOyfw8Dh1sQnvlGLFSAHcMcjXs0YJKfF9VI4EsFnruD_NF0PUcy519zur_5g3e31kj4WfFTDSnnlJTaZIwuu.61lQVFI3HKnRySCi2MpEPSZyae2YCyw0PThJSOsXIipdyLMjMSbyvm2N3D0OCg17v8RytnSwmzWTacJDcr3qXKXM2HMNI0dITsBGTOSAoemPK2XljEZISKIEPjekgNpUpIkZeUzPiiVCKLxC6OY_CWAAChtb3RRT60rWJMwiy6t9fSKzGNWZlGQv5ujjSZFQxuW0K1mfQaRfr5Q2Qox4.yEZN5o4K6mh_PGaCPmhBoj1QKVUDnMIaVK8wnt58SV4zbWGRQknpFJzFV7RxbPjxaIyqbubtibCkVDQ8lEoQu7YnjV3ydDz_Yp2d80K5yncJSmhPM5EyWBwQl11fOQ84LtL6XjVbQTqdZ30VWWODJPnzxUgq5qo3O6Tg_kZ5PKoZn.IPBJwquZDSePQFvTDozqTPLKWs75YwKcPxieyipqLlAbHSWIPxcyDb7aC7YjZcxnCZQy8MFSkb21Vk5cxbdNt9Q1O53Ed4iCUKf73HqTRi2wP.DowLZ31O7VxtO.ISsFGzf.kpb0OqYcxD00XNvO6cyl6DiJY4pgWZTyVnaCxenzWZ7MMawdT8bs1fmEvAR.lySXIohHCNK5mEswftrKzT2yvZ5i9nNgASzEtR8G1ATpxaMq6C0JjdCAsMdLKepkrHKX4W3yw_b2jBPDxN_BTdIIHZ9AiMCnyOvtDDad42OGIjvjePqM8_wZXD5jgTp_xHQ5RP3ddUzd.jzrm0DikmVdu8yxBGhRDCW_fcpF59MxI2QQLa84qYXjVbgxHyw8Ut.PlZP_yrzQv6A8qxsnssJUOGQeKlkEXjqPNsEfnXPAK952CA0N7nGJ_0w6py4tbeUx2jfok2I72GGPy_G.BBHPq9kuKYGhVdZPA9whmn_vNS.smsDXuZ__eM48DlWDRVcy7G7ozgrdKU_ae2NmxvIKJJSowf8O1RHOJYoBoXbtRm6_43m3DU2g.5ocwy0LquVjUjRggwbzl',
            'whatsSelect': '1',
            'roomType': '00',
            'dwAll': 'N',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': token[0].group(1)
        }
        try:
            response = requests.post(url=submit_url, data=data, headers=req.headers, proxies=req.proxies)
        except Exception as e:
            raise Exception('提交订单失败, 错误信息: %s' % str(e))
        else:
            if '余票不足' in response.text:
                print('余票不足!')
                return False
            else:
                print('抢票成功')
                return True

    """ 查询待支付订单 """
    def queryMyOrderNoComplete(self):
        try:
            no_complete_url = QUERY_MY_ORDER.get('url')
            data = {
                '_json_att:': ''
            }
            req.headers['Referer'] = INIT_DC.get('url')
            info_dict = {}
            response = requests.post(url=no_complete_url, data=data, headers=req.headers, proxies=req.proxies)
            jsdata = json.loads(response.text)['data']['orderDBList'][0]
            info_dict['姓名：'] = jsdata['array_passser_name_page'][0]         # 姓名
            info_dict['出发地：'] = jsdata['from_station_name_page'][0]        # 出发地
            info_dict['目的地：'] = jsdata['to_station_name_page'][0]          # 目的地
            info_dict['出发日期：'] = jsdata['start_train_date_page'].split(' ')[0]             # 出发日期
            info_dict['订单号：'] = jsdata['sequence_no']                   # 订单号
            info_dict['价格：'] = jsdata['ticket_total_price_page']         # 价格
            info_dict['出发时间：'] = jsdata['start_time_page']             # 出发时间
            info_dict['到达时间：'] = jsdata['arrive_time_page']            # 到达时间
            info_dict['车次：'] = jsdata['train_code_page']                 # 车号
            tickets = jsdata['tickets'][0]
            a = tickets['coach_name']                   # 车厢
            b = tickets['seat_name']                    #座位号
            info_dict['列车信息：'] = a + '车' + b
            info_dict['座位性质：'] = tickets['seat_type_name']          # 座位性质
            info_dict['支付时间：'] = tickets['reserve_time']            # 支付时间
            info_dict['到期时间：'] = tickets['pay_limit_time']          # 到期时间
            return info_dict
        except Exception as e:
            raise Exception('没有查询到待支付订单. %s' % str(e))

    """ 查询是否抢购成功 """
    def check_play(self):
        i = 0
        while True:
            time.sleep(0.3)
            i += 1
            try:
                d_play = self.queryMyOrderNoComplete()
                cc = d_play['车次：']
                rt = 'True'
                break
            except:
                if i > 5:
                    rt = 'False'
                    break

        if rt == 'True':
            # 抢票成功
            return True
        if rt == 'False':
            # 抢票失败
            return False

    def canal_brush(self):
        print('取消订单')
