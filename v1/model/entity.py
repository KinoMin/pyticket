class InputInfo(object):
    """
    封装用户输入信息
    passengers: 用户姓名
    from_time: 乘车日期
    from_input: 起始站
    to_input: 终点站
    seat_type: 座位类型
    number_input: 抢票车次
    """
    def __init__(self, passengers, from_time, from_input, to_input, seat_type, train_number, scope_time):
        self.passengers = passengers
        self.from_time = from_time
        self.from_input = from_input
        self.to_input = to_input
        self.seat_type = seat_type
        self.train_number = train_number
        self.scope_time = scope_time

class Train(object):
    def __init__(self, secret_str, query_time, train_num, first_seat, second_seat, start_data, end_date, from_station, to_station, train_no, start_local):
        self.secret_str = secret_str
        self.query_time = query_time
        self.train_num = train_num
        self.first_seat = first_seat
        self.second_seat = second_seat
        self.start_data = start_data
        self.end_date = end_date
        self.from_station = from_station
        self.to_station = to_station
        self.train_no = train_no,
        self.start_local = start_local