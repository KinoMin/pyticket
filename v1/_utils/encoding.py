"""
解决 requests 返回中文乱码
"""

import chardet
import re

def encoding(response_obj:object)->str:
    """
    Automatically parse web page encoding
        First parse the charset from the response header
        Then parse from the response data
    :param response_obj: REQUEST RESPONSE OBJECT
    :return: Coding
    """
    charset_header = response_obj.headers["Content-Type"]
    pattern_charset_header = re.compile('charset=(.*)', re.I)
    charset = re.search(pattern_charset_header, charset_header)
    if charset is not None:
        return charset.groups()[0]
    else:
        charset = chardet.detect(response_obj.content)["encoding"]
        return charset