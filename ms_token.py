# _*_ coding:utf-8 _*_
'''"""
作者：cai
日期：2024年11月18日
一个mstoken的库
“”“'''
import random
import re

def generate_random_mstoken(randomlength=172):
    """
    根据传入长度产生随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789='
    length = len(base_str) - 1
    for _ in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


import json
import random
import sys
import time
import threading
from urllib.parse import urlparse, urlunparse

import requests
# from fake_useragent import UserAgent

# from CookieUtil import CookieUtil


#它是通过向字节跳动的接口发送POST请求，并从响应的cookie中提取`ttwid`值。
def get_ttwid(user_agent):
    headers = {
        "User-Agent": user_agent,
        "Content-Type": "application/json"
    }
    request_url = "https://ttwid.bytedance.com/ttwid/union/register/"

    data = {
        "aid": 2906,
        "service": "douyin.com",
        "unionHost": "https://ttwid.bytedance.com",
        "needFid": "false",
        "union": "true",
        "fid": ""
    }

    data_str = json.dumps(data)
    response = requests.post(request_url, data=data_str, headers=headers)

    jsonObj = json.loads(response.text)
    callback_url = jsonObj['redirect_url']
    response = requests.get(callback_url, headers=headers)
    status_code = response.status_code
    if status_code == 200 and 'Set-Cookie' in response.headers:
        cookie_dict = response.headers['Set-Cookie']
        if "ttwid" in cookie_dict:
            # return cookie_dict['ttwid']
            match = re.search(r"ttwid=([^;]+)", cookie_dict)
            if match:
                ttwid_value = match.group(1)
                return ttwid_value
    return None

# 这个函数用于获取`__ac_nonce`，它是通过向视频页面发送GET请求，并从响应的cookie中提取`__ac_nonce`。
def get_ac_nonce(user_agent, url):
    headers = {
        'user-agent': user_agent
    }
    __ac_nonce = requests.get(url, headers=headers).cookies.get('__ac_nonce')
    print(__ac_nonce)
    return __ac_nonce

# `count_to_text` 和 `big_count_operation`：这两个函数用于执行一些位操作和字符编码，生成`ac_signature`的一部分。
def count_to_text(deci_num, ac_signature):
    off_list = [24, 18, 12, 6, 0]
    for value in off_list:
        key_num = (deci_num >> value) & 63
        if key_num < 26:
            val_num = 65
        elif key_num < 52:
            val_num = 71
        elif key_num < 62:
            val_num = -4
        else:
            val_num = -17
        ascii_code = key_num + val_num
        ac_signature += chr(ascii_code)
    return ac_signature
def big_count_operation(string, final_num):
    for char in string:
        char_code_count = ord(char)
        final_num = ((final_num ^ char_code_count) * 65599) & 0xFFFFFFFF  # Use & to simulate the behavior of >>> 0
    return final_num

#load_ac_signature`：这个函数用于生成`ac_signature`，它是通过一系列的位操作和编码操作，结合URL、时间戳、用户代理等信息生成的。
def load_ac_signature(url, ac_nonce, ua):
    final_num = 0
    temp = 0
    ac_signature = "_02B4Z6wo00f01"
    # Get the current timestamp
    time_stamp = str(int(time.time() * 1000))

    # Perform big count operation on timestamp
    final_num = big_count_operation(time_stamp, final_num)

    # Perform big count operation on the URL
    url_num = big_count_operation(url, final_num)
    final_num = url_num

    # Create a 32-bit binary string from a combination of operations
    long_str = bin(((65521 * (final_num % 65521) ^ int(time_stamp)) & 0xFFFFFFFF))[2:]
    while len(long_str) != 32:
        long_str = "0" + long_str

    # Create a binary number and parse it into decimal
    binary_num = "10000000110000" + long_str
    deci_num = int(binary_num, 2)

    # Perform countToText operations
    ac_signature = count_to_text(deci_num >> 2, ac_signature)
    ac_signature = count_to_text((deci_num << 28) | 515, ac_signature)
    ac_signature = count_to_text((deci_num ^ 1489154074) >> 6, ac_signature)

    # Perform operation for the 'aloneNum'
    alone_num = (deci_num ^ 1489154074) & 63
    alone_val = 65 if alone_num < 26 else 71 if alone_num < 52 else -4 if alone_num < 62 else -17
    ac_signature += chr(alone_num + alone_val)

    # Reset final_num and perform additional operations
    final_num = 0
    deci_opera_num = big_count_operation(str(deci_num), final_num)
    final_num = deci_opera_num
    nonce_num = big_count_operation(ac_nonce, final_num)
    final_num = deci_opera_num
    big_count_operation(ua, final_num)

    # More countToText operations
    ac_signature = count_to_text((nonce_num % 65521 | ((final_num % 65521) << 16)) >> 2, ac_signature)
    ac_signature = count_to_text(
        (((final_num % 65521 << 16) ^ (nonce_num % 65521)) << 28) | (((deci_num << 524576) ^ 524576) >> 4),
        ac_signature)
    ac_signature = count_to_text(url_num % 65521, ac_signature)

    # Final temp operations and appending to ac_signature
    for i in ac_signature:
        temp = ((temp * 65599) + ord(i)) & 0xFFFFFFFF

    last_str = hex(temp)[2:]
    ac_signature += last_str[-2:]

    return ac_signature


#`get_trace_id`：这个函数生成一个UUID，用于追踪请求
def get_trace_id():
    t = int(time.time() * 1000)  # 获取当前时间的毫秒数
    e = int((time.perf_counter() if hasattr(time, 'perf_counter') else 0) * 1000)  # 获取性能时间的毫秒数

    uuid_template = "xxxxxxxx"
    uuid = []

    for char in uuid_template:
        if char == 'x':
            r = int(16 * random.random())
            if t > 0:
                r = (t + r) % 16
                t = t // 16
            else:
                r = (e + r) % 16
                e = e // 16
            uuid.append(format(r, 'x'))
        else:
            r = int(16 * random.random())
            uuid.append(format((3 & r) | 8, 'x'))

    return ''.join(uuid)

# #do_add_view_count`：这个函数用于增加单个视频的播放次数。它通过构造一系列的请求参数和数据，向抖音的接口发送POST请求。
# def do_add_view_count(video_url):
#     ua = UserAgent(platforms=['pc'], os=["windows", "macos"])
#     user_agent = ua.chrome
#
#     parsed_url = urlparse(video_url)
#     url_without_query = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
#     print("url_without_query: \n", url_without_query)
#
#     aweme_id = url_without_query.split('/')[-1]
#     print(aweme_id)
#
#     ttwid = get_ttwid(user_agent)
#     web_id = get_web_id(user_agent)
#     ms_token = get_ms_token()
#     biz_trace_id = get_trace_id()
#
#     ac_nonce = get_ac_nonce(user_agent, url_without_query)
#     ac_signature = load_ac_signature(url_without_query, ac_nonce, user_agent)
#
#     print("ttwid: \n", ttwid)
#     print("web_id: \n", web_id)
#     print("ac_nonce: \n", ac_nonce)
#     print("ac_signature: \n", ac_signature)
#
#     cookie_content = f"ttwid={ttwid}; msToken={ms_token}; webid={web_id}; __ac_nonce={ac_nonce}; __ac_signature={ac_signature}; biz_trace_id={biz_trace_id}"
#
#     request_url = "https://www.douyin.com/aweme/v2/web/aweme/stats/"
#
#     request_params = {
#         "device_platform": "webapp",
#         "aid": 6383,
#         "channel": "channel_pc_web",
#         "pc_client_type": 1,
#         "pc_libra_divert": "Mac",
#         "update_version_code": 170400,
#         "version_code": 170400,
#         "version_name": "17.4.0",
#         "cookie_enabled": "true",
#         "screen_width": 1440,
#         "screen_height": 900,
#         "browser_language": "zh - CN",
#         "browser_platform": "MacIntel",
#         "browser_name": "Chrome",
#         "browser_version": "129.0.0.0",
#         "browser_online": "true",
#         "engine_name": "Blink",
#         "engine_version": "129.0.0.0",
#         "os_name": "Mac + OS",
#         "os_version": "10.15.7",
#         "cpu_core_num": 8,
#         "device_memory": 8,
#         "platform": "PC",
#         "downlink": 10,
#         "effective_type": "4g",
#         "round_trip_time": 50,
#         "webid": web_id,
#         "msToken": ms_token
#     }
#
#     request_data = {
#         "aweme_type": 0,
#         "item_id": aweme_id,
#         "play_delta": 1,
#         "source": 0
#     }
#
#     headers = {
#         'origin': 'https://www.douyin.com',
#         'referer': 'https://www.douyin.com/video/7418851799752264997',
#         'user-agent': user_agent,
#         'Cookie': cookie_content,
#         'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
#     }
#
#     response = requests.post(request_url, params=request_params, data=request_data, headers=headers)
#
#     print(response.status_code)
#     print(response.text)
#
# #`add_view_count`：这个函数用于多次调用`do_add_view_count`函数，以增加指定次数的播放次数。
# def add_view_count(video_url, view_count):
#     for i in range(view_count):
#         do_add_view_count(video_url)
#
# # `parallel_add_view_count`：这个函数使用多线程来并行增加视频的播放次数，以提高效率。
# def parallel_add_view_count(video_url, view_count):
#     threads = []
#     thread_num = 1
#     if view_count < thread_num:
#         thread_num = 1
#         count_in_per_thread = view_count
#     else:
#         count_in_per_thread = (view_count + thread_num - 1) // thread_num
#     for i in range(thread_num):
#         thread = threading.Thread(target=add_view_count, args=(video_url, count_in_per_thread,))
#         threads.append(thread)
#         thread.start()
#
#     for thread in threads:
#         thread.join()
#
#     print("所有请求已完成^_^")


if __name__ == '__main__':
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    url = "https://www.douyin.com/aweme/v1/web/aweme/post/"
    ttwid = get_ttwid(ua)
    print(ttwid)

    pass

