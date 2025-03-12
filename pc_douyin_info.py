# _*_ coding:utf-8 _*_
'''"""
作者：cai
日期：2024年12月27日
爬取抖音的信息
“”“'''
import requests
import urllib.parse
from functools import partial
import subprocess

subprocess.Popen = partial(subprocess.Popen,encoding="utf-8")
import execjs
import random
import json
import os
import re
import time
from datetime import datetime, timedelta
import pandas as pd
import datetime
from DouyinVideoDB import DouyinVideo           #视频信息数据库
from DouyinAccountDB import DouyinAccount       #作者信息数据库
from DouyinVideoDataDB import DouyinVideoData   #视频信息详情数据库
from MinIoClient import MinioClient             #minio操作，把图片上传到minio


#生成mstoken
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

#获得headers的
def get_header():
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'SEARCH_RESULT_LIST_TYPE=%22single%22; hevc_supported=true; fpk1=U2FsdGVkX18v72dISLDqb1RsAuRYsygVs9dsq2u0LFVKupbgt0djKGFkEDsIFgK62w5sTWfas5HKjcAQ1MDWPw==; fpk2=7675d59b5e84e0a878ee6f0a97f9056f; odin_tt=59da35b12d97d9d44910c5791d09f360064daa841ea48e8409d62011625257561523a01f00196252edec566cebcd6289590d1d3599132c0db74bd3d57f226edbd5d13a60bd7cbaaabd8c22803f631cfa; bd_ticket_guard_client_web_domain=2; passport_csrf_token=4d19a24a0d12e546a38a82cb1dd69d9c; passport_csrf_token_default=4d19a24a0d12e546a38a82cb1dd69d9c; UIFID=63bdc4b4b456901f349a081bfd3a24da10a1c6623f0a2d5eadd83f51c9f4d1123e3e881c56f5c5c435ebd0a12a8a9b7056ae64added34f6177501a2c86a624823ee63c1e1189427b288602a280743f12777b39b10b7e07b5704d3065525da753e2eac54a5d7aa41e04f96816347e74e8fe0430e9a92c601f70ab1e81413739ddc2ebe139901f83a48139c9f34001c042785d0d16e68aada1d0b2c3e0d8b16830; s_v_web_id=verify_m3gouxy4_4wez48DB_8epu_4EvO_8obD_dXEFpX0M3R6G; xgplayer_user_id=706813208332; ttwid=1%7Cz6TOkDyq3pu4ONaIu1ika9jr7hRFaUBRad9UcDN2qDQ%7C1733724486%7C3ee897fec2a66093532809a24a2bb7528d64d4493a0ae99621ae0b1027ef18ed; passport_mfa_token=Cje%2FtpmiRwJKb1JIB9x8rUG6ui3ZvUKKAPCN4q%2FnE5NCNLN%2FySe8sgGcDIjpH5axQ6xUT3Kvb2uSGkoKPG91oBnWzSBc7jX%2FlFjT%2FMH01cLcvrV4SNylAaf0L8dUw3jFDielsK%2Fu9TOMhKj5xtz8AS5uf%2F%2BD0PMX3BD6z%2BMNGPax0WwgAiIBA9Rm4HI%3D; dy_swidth=1920; dy_sheight=1080; is_dash_user=1; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D; theme=%22dark%22; manual_theme=%22dark%22; download_guide=%223%2F20250108%2F0%22; __security_mc_1_s_sdk_crypt_sdk=68a6add1-4d4c-8a66; __security_mc_1_s_sdk_cert_key=e23ca1ed-4ea2-b544; __security_mc_1_s_sdk_sign_data_key_web_protect=c5e3c9f4-46ad-b78b; __security_mc_1_s_sdk_sign_data_key_sso=9f00316a-4331-8629; WallpaperGuide=%7B%22showTime%22%3A1736408353602%2C%22closeTime%22%3A1735814490900%2C%22showCount%22%3A5%2C%22cursor1%22%3A132%2C%22cursor2%22%3A40%2C%22hoverTime%22%3A1735792238712%7D; __ac_nonce=06780835f00378edb7ec2; __ac_signature=_02B4Z6wo00f01LTgdjAAAIDBa7uFfmpeWYy0wHKAAEq99a; douyin.com; device_web_cpu_core=4; device_web_memory_size=8; architecture=amd64; IsDouyinActive=true; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A4%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A2.2%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A250%7D%22; csrf_session_id=bae4fbf4f3ab328a99d6539bef7584f1; strategyABtestKey=%221736475491.676%22; home_can_add_dy_2_desktop=%221%22; biz_trace_id=256a48ee; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTUR0MFRsNmZ1cVBXRHdsbU1vL3ZBY1JOSnRMcitzMUp1OXNXODZjVldpUTVBVGVSWCtLa3F1enZyMDFIb1FGUE5ZL0svaVBqNDdrNnFpY3czWmpweUk9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; sdk_source_info=7e276470716a68645a606960273f276364697660272927676c715a6d6069756077273f276364697660272927666d776a68605a607d71606b766c6a6b5a7666776c7571273f275e58272927666a6b766a69605a696c6061273f27636469766027292762696a6764695a7364776c6467696076273f275e5827292771273f27333035303c31303231333632342778; bit_env=PoUDGFZonkJVyYkFt7zyZyzaWEOnb5PM1KEq3lb8JYYjicHniUVAdGtiA527eggNTVb8yfJVtMYNeE_ElDK21J1u9DjBiDHUoM1lM7EasY-MrNP8-9m6_CuWDWyRYncgZN5aO_urPePGoz78R8Xep9kwHP5f-QiugXf8oc79Ifh4h84xi8blhOn1gzueMv6ovzvEG3J2GgjyPYGGRdrSw6gO0emI7vId7lBAKT5QzhtZvsmVosM7H6hIUx4rVNKWZGcTwEzd6bIzlHNpam3i7vmjsuqFc9thHniXkPIHqls8hPFom5bSP2OCXrS9FFPhz5FBaLxh_UUN54-Eh9yi6HqF0Zn54OMiyLaIwif-3eltvkhYPHOIKzSvTOr7gJUXqlhnsq9QLUmaFefw7Fo7hdmq_TrSHjmasofChVquBWbKkm4vjyFEzE8geStV3_H8rR7DHTNFutR0GD8QrFbr9EzOpLatu10xj9auIHrt0ERvetnv_tsv_ZheNZu4CklO; gulu_source_res=eyJwX2luIjoiNGEyZmE1ZTg5YTg1M2ViNDJiOTRmMzNjODI3MThlYzAyMDdmNDc5ZjdhYTgxNmE5ZjlmZmNjNmI3OGFhZWZmNiJ9; passport_auth_mix_state=wrpzulwosq9kb1xj73up9uqcobzfhyq5jk2v26ksuquba7of; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.182%7D; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A1%7D%22; xg_device_score=7.124006546909391',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.douyin.com/?recommend=1',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'uifid': '63bdc4b4b456901f349a081bfd3a24da10a1c6623f0a2d5eadd83f51c9f4d1123e3e881c56f5c5c435ebd0a12a8a9b7056ae64added34f6177501a2c86a624823ee63c1e1189427b288602a280743f12777b39b10b7e07b5704d3065525da753e2eac54a5d7aa41e04f96816347e74e8fe0430e9a92c601f70ab1e81413739ddc2ebe139901f83a48139c9f34001c042785d0d16e68aada1d0b2c3e0d8b16830',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }
    return headers

#拿到a_bogus的值
def get_a_bogus(params,ua,data = None):
    pa = urllib.parse.urlencode(params)
    # da = urllib.parse.urlencode(data)
    da = None
    ua = get_header()['user-agent']

    with open('cun.js', encoding='utf-8') as f:
        first_js = execjs.compile(f.read())

    sign = first_js.call('enc', pa, da, ua)
    # print(sign["abogus"])
    return sign["abogus"]
    pass

#分割出desc的
def split_desc(desc):
    # 使用正则表达式检查是否有标签（#）
    match = re.match(r'^(.*?)(#.*)?$', desc)

    # 提取前面和后面的部分
    if match:
        text_before_hash = match.group(1).strip()  # '#' 前的文本
        text_after_hash = match.group(2).strip() if match.group(2) else ""  # '#' 后的文本，如果没有 '#'，则为空字符串
    else:
        text_before_hash = ""
        text_after_hash = ""

    # 输出结果
    return {
        "description":text_before_hash,
        "tags":text_after_hash
    }

#分割url的
def splpt_url(url):
    # 正则表达式匹配用户ID和视频ID
    match = re.search(r'/user/([A-Za-z0-9_-]+)', url)

    if match:
        sec_user_id = match.group(1)  # 提取用户ID
        # locate_item_id = match.group(2)  # 提取视频ID
        return {"sec_user_id":sec_user_id}#,"locate_item_id":locate_item_id}
    else:
        print("No match found")
        return None
    pass

#分割出sec_uid的
def extract_sec_uid(url):
    # 正则表达式匹配 sec_uid 参数
    match = re.search(r"sec_uid=([A-Za-z0-9_-]+)", url)
    if match:
        return match.group(1)
    else:
        return None

#读取文件的
def read_xlsx():
    # 读取 Excel 文件
    file_path = 'YT_sorce_pet.xlsx'

    # 使用 pandas 读取 Excel 文件
    df = pd.read_excel(file_path)

    # 提取 "达人链接" 列的数据
    if '达人链接' in df.columns:
        da_ren_lianjie = df['达人链接']
        return da_ren_lianjie
    else:
        print("没有找到 '达人链接' 这一列")
        return None

#拿到请求的返回值
def get_video_json(sec_user_id,max_cursor,short_id,url):
    '''
    :param sec_user_id: 每位作者的user_id的加密值乱码？可以确定的是，这是固定的
    :param locate_item_id: 这个不唯一，每位作者的作品里边的这个请求值不同
    :param max_cursor: 这个是翻页请求码，一般来说是从0开始，每次请求返回的text里面都有这个值，拿这个值再去请求可以得到之后的视频
    :return:
    '''
    dyv = DouyinVideo()         #抖音视频信息数据库操作
    dyvd = DouyinVideoData()    #抖音视频详情信息
    count = 20
    params = {
        'device_platform': 'webapp',
        'aid': '6383',
        'channel': 'channel_pc_web',
        'sec_user_id': f'{sec_user_id}',
        'max_cursor': f'{max_cursor}',
        # 'locate_item_id': f'{locate_item_id}',
        'locate_query': 'false',
        'show_live_replay_strategy': '1',
        'need_time_list': '0',
        'time_list_query': '0',
        'whale_cut_token': '',
        'cut_version': '1',
        'count': f'{count}',
        'publish_video_strategy_type': '2',
        'from_user_page': '0',
        'update_version_code': '170400',
        'pc_client_type': '1',
        'pc_libra_divert': 'Windows',
        'version_code': '290100',
        'version_name': '29.1.0',
        'cookie_enabled': 'true',
        'screen_width': '1920',
        'screen_height': '1080',
        'browser_language': 'zh-CN',
        'browser_platform': 'Win32',
        'browser_name': 'Chrome',
        'browser_version': '130.0.0.0',
        'browser_online': 'true',
        'engine_name': 'Blink',
        'engine_version': '130.0.0.0',
        'os_name': 'Windows',
        'os_version': '10',
        'cpu_core_num': '4',
        'device_memory': '8',
        'platform': 'PC',
        'downlink': '10',
        'effective_type': '4g',
        'round_trip_time': '0',
        'webid': '7436948931495986740',
        'uifid': '63bdc4b4b456901f349a081bfd3a24da10a1c6623f0a2d5eadd83f51c9f4d1123e3e881c56f5c5c435ebd0a12a8a9b709c3a331cdef00eaf1537f691d6d6e3959e20abfe2bea8736f4d56e22cd2fff4273f25b8150f2c9cd61a8611ea4cd5ff4142e603181c5ff2084d56407df8ed810ce5debeba138cb050061c3033dddc6f48fbf6129005fc7943c632dd1ccf245bf9349b89208f85c84af4d56a1c652b48b',
        'msToken': f'{generate_random_mstoken()}',
        # 'a_bogus': 'QX4nDtUwDx8RFVMSYKjAyWQlQ92ArsSyT-TOSS3PyPzMbXFPtSPgiNeXcozKUBU-XWpsie37BntAbndcMzUiZqHpwmpkuTXbrU/cVumL/qZfY-vZ7HmxCJbEFiPGUCGYuQIXEMv5lsMe2DQWIq9hABMHL/lNRcfdBN3tV2TnO9KsUSWjho/Aa-GdN7JqnE==',
        'verifyFp': 'verify_m3im954a_yUHqTe05_wKqA_4X86_9iVR_nagNcXVQ36Ga',
        'fp': 'verify_m3im954a_yUHqTe05_wKqA_4X86_9iVR_nagNcXVQ36Ga',
    }
    # da = urllib.parse.urlencode(data)
    da = None
    ua = get_header()['user-agent']


    params['a_bogus'] = get_a_bogus(params,ua)
    response = requests.get('https://www.douyin.com/aweme/v1/web/aweme/post/', params=params, headers=get_header())
    # print(response.text)
    resp_json = response.json()
    aweme_list = resp_json['aweme_list']
    if aweme_list == None or aweme_list == []:
        return None
    for aweme in aweme_list:
        aweme_id = aweme['aweme_id']                #作品id
        create_time = aweme['create_time']          #作品发布时间
        desc = aweme['desc']                        #视频说明和标签
        desc_dist = split_desc(desc)
        description = desc_dist['description']      #视频说明
        tags = desc_dist['tags']                    #视频标签
        statistics = aweme['statistics']            #详情页相关的信息
        collect_count = statistics['collect_count'] #收藏数
        comment_count = statistics['comment_count'] #评论数
        digg_count = statistics['digg_count']       #点赞数
        share_count = statistics['share_count']     #转发数
        page_url = url+f"?modal_id={aweme_id}"
        cover_url = aweme['video']['cover']['url_list'][-1] #图片，封面图

        create_time = datetime.utcfromtimestamp(int(create_time)).strftime('%Y-%m-%d %H:%M:%S')
        print("开始插入视频数据")
        dyv.upsert(aweme_id,short_id,desc,create_time,description,tags,page_url,str(aweme))
        print("插入视频数据完成，开始插入视频详情数据")
        dyvd.insert(aweme_id,digg_count,comment_count,collect_count,share_count,str(statistics))
    print(short_id,"完成")
    pass

#作者信息
def get_author_info_json(sec_user_id,url):
    dya = DouyinAccount()
    params = {
        'device_platform': 'webapp',
        'aid': '6383',
        'channel': 'channel_pc_web',
        'publish_video_strategy_type': '2',
        'source': 'channel_pc_web',
        'sec_user_id': f'{sec_user_id}',
        'personal_center_strategy': '1',
        'profile_other_record_enable': '1',
        'land_to': '1',
        'update_version_code': '170400',
        'pc_client_type': '1',
        'pc_libra_divert': 'Windows',
        'version_code': '170400',
        'version_name': '17.4.0',
        'cookie_enabled': 'true',
        'screen_width': '1920',
        'screen_height': '1080',
        'browser_language': 'zh-CN',
        'browser_platform': 'Win32',
        'browser_name': 'Chrome',
        'browser_version': '131.0.0.0',
        'browser_online': 'true',
        'engine_name': 'Blink',
        'engine_version': '131.0.0.0',
        'os_name': 'Windows',
        'os_version': '10',
        'cpu_core_num': '4',
        'device_memory': '8',
        'platform': 'PC',
        'downlink': '1.35',
        'effective_type': '3g',
        'round_trip_time': '650',
        'webid': '7436948931495986740',
        'uifid': '63bdc4b4b456901f349a081bfd3a24da10a1c6623f0a2d5eadd83f51c9f4d1123e3e881c56f5c5c435ebd0a12a8a9b7056ae64added34f6177501a2c86a624823ee63c1e1189427b288602a280743f12777b39b10b7e07b5704d3065525da753e2eac54a5d7aa41e04f96816347e74e8fe0430e9a92c601f70ab1e81413739ddc2ebe139901f83a48139c9f34001c042785d0d16e68aada1d0b2c3e0d8b16830',
        'verifyFp': 'verify_m3gouxy4_4wez48DB_8epu_4EvO_8obD_dXEFpX0M3R6G',
        'fp': 'verify_m3gouxy4_4wez48DB_8epu_4EvO_8obD_dXEFpX0M3R6G',
        'msToken':  f'{generate_random_mstoken()}',
        # 'a_bogus': 'QfsVk77wO2W5CdKSYCJF9jKloZ2MNBuy5lTQWxnPCxYbGwzYMSNNwNCrnxuNsFuSCuBswo1HVEzAYDncQUUkZe9kzmkvSdiSbG/AI7vo2Zi2Tsk2vqmKCbbxqiTbUW4Y85IXEMf5IsMe2EQWVN9iAdM7F/Uxm5EdFr3UV/YjY9KsUC8jh92na3XQwh6D',
    }
    ua = get_header()['user-agent']
    params['a_bogus'] = get_a_bogus(params,ua)
    response = requests.get('https://www.douyin.com/aweme/v1/web/user/profile/other/', params=params, headers=get_header())
    resp_json = response.json()
    user = resp_json['user']
    try:
        aweme_count = user['aweme_count']                               #作品数量
    except:
        print("该作者没有作品，可能这个人注销了账号")
        return None
    nickname = user['nickname']                                     #作者名字
    signature = user['signature']                                   #介绍
    short_id = user['short_id']                                     #抖音号
    if short_id == "0" or short_id == "":
        short_id = user['unique_id']
    total_favorited = user['total_favorited']                       #总的点赞数
    # user_age = user['user_age']                                     #年龄
    mplatform_followers_count = user['mplatform_followers_count']   #粉丝数
    try:
        account_cert_info = json.loads(user['account_cert_info'])['label_text'] #认证身份
    except:
        account_cert_info = ""
    print(f"开始插入{nickname}作者信息")
    dya.upsert(nickname,account_cert_info,mplatform_followers_count,total_favorited,aweme_count,short_id,signature,url,str(user))

    return short_id

#上传到minio
def set_into_minio(cover_url,aweme_id):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'SEARCH_RESULT_LIST_TYPE=%22single%22; hevc_supported=true; fpk1=U2FsdGVkX18v72dISLDqb1RsAuRYsygVs9dsq2u0LFVKupbgt0djKGFkEDsIFgK62w5sTWfas5HKjcAQ1MDWPw==; fpk2=7675d59b5e84e0a878ee6f0a97f9056f; odin_tt=59da35b12d97d9d44910c5791d09f360064daa841ea48e8409d62011625257561523a01f00196252edec566cebcd6289590d1d3599132c0db74bd3d57f226edbd5d13a60bd7cbaaabd8c22803f631cfa; bd_ticket_guard_client_web_domain=2; passport_csrf_token=4d19a24a0d12e546a38a82cb1dd69d9c; passport_csrf_token_default=4d19a24a0d12e546a38a82cb1dd69d9c; UIFID=63bdc4b4b456901f349a081bfd3a24da10a1c6623f0a2d5eadd83f51c9f4d1123e3e881c56f5c5c435ebd0a12a8a9b7056ae64added34f6177501a2c86a624823ee63c1e1189427b288602a280743f12777b39b10b7e07b5704d3065525da753e2eac54a5d7aa41e04f96816347e74e8fe0430e9a92c601f70ab1e81413739ddc2ebe139901f83a48139c9f34001c042785d0d16e68aada1d0b2c3e0d8b16830; s_v_web_id=verify_m3gouxy4_4wez48DB_8epu_4EvO_8obD_dXEFpX0M3R6G; xgplayer_user_id=706813208332; ttwid=1%7Cz6TOkDyq3pu4ONaIu1ika9jr7hRFaUBRad9UcDN2qDQ%7C1733724486%7C3ee897fec2a66093532809a24a2bb7528d64d4493a0ae99621ae0b1027ef18ed; passport_mfa_token=Cje%2FtpmiRwJKb1JIB9x8rUG6ui3ZvUKKAPCN4q%2FnE5NCNLN%2FySe8sgGcDIjpH5axQ6xUT3Kvb2uSGkoKPG91oBnWzSBc7jX%2FlFjT%2FMH01cLcvrV4SNylAaf0L8dUw3jFDielsK%2Fu9TOMhKj5xtz8AS5uf%2F%2BD0PMX3BD6z%2BMNGPax0WwgAiIBA9Rm4HI%3D; dy_swidth=1920; dy_sheight=1080; is_dash_user=1; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D; theme=%22dark%22; manual_theme=%22dark%22; WallpaperGuide=%7B%22showTime%22%3A1736148248103%2C%22closeTime%22%3A1735814490900%2C%22showCount%22%3A4%2C%22cursor1%22%3A95%2C%22cursor2%22%3A28%2C%22hoverTime%22%3A1735792238712%7D; __ac_nonce=0677ddc040082ea951bde; __ac_signature=_02B4Z6wo00f010BGcAgAAIDCnx2DRflxhJ9AZnSAALd3b6; douyin.com; xg_device_score=6.953669239252326; device_web_cpu_core=4; device_web_memory_size=8; architecture=amd64; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A4%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A1.45%2C%5C%22effective_type%5C%22%3A%5C%223g%5C%22%2C%5C%22round_trip_time%5C%22%3A300%7D%22; csrf_session_id=bae4fbf4f3ab328a99d6539bef7584f1; strategyABtestKey=%221736301576.99%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.182%7D; home_can_add_dy_2_desktop=%221%22; biz_trace_id=16dae0e9; gulu_source_res=eyJwX2luIjoiNGEyZmE1ZTg5YTg1M2ViNDJiOTRmMzNjODI3MThlYzAyMDdmNDc5ZjdhYTgxNmE5ZjlmZmNjNmI3OGFhZWZmNiJ9; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTUR0MFRsNmZ1cVBXRHdsbU1vL3ZBY1JOSnRMcitzMUp1OXNXODZjVldpUTVBVGVSWCtLa3F1enZyMDFIb1FGUE5ZL0svaVBqNDdrNnFpY3czWmpweUk9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; download_guide=%221%2F20250108%2F0%22; sdk_source_info=7e276470716a68645a606960273f276364697660272927676c715a6d6069756077273f276364697660272927666d776a68605a607d71606b766c6a6b5a7666776c7571273f275e58272927666a6b766a69605a696c6061273f27636469766027292762696a6764695a7364776c6467696076273f275e5827292771273f27323032363335373536333632342778; bit_env=zHjrcu_250Bt-FM4lBQYlaKClRArQ99DKVRipG_v1YfxUZ8C0qhbOtF3v7ikB8QyzC340jzoJVLXaLqq5yUrMxAqJAxTp8exeAw0Zq_ZBXsT1SmoHS5fLXqpr59zDdLJgZL7r6MF8_NDd6V4NNp-tgF6rdiPa6DmN1jsk2r7oR7PNsnmvc_k7EfSuzLfobhljj95AB5wZPpIA-Lsb-T-J2Wa_JVOCYnu3F_ZjSytkkVGjD0CzU84G1UeLJO6HlWM_8myjnRR3-GcVYM_jhPMPzMH6gS7uO7EIHfLd_eUlj3TTEJKO1CthfGvpKORctOwyTDbNz8hxOoTOfl4vTfS8x0RNlCTGHHRbwXvnqOT-Nhmkd3caj5OVJaE7o5BAzATAquRwwpK6dkxDa4EYwdr-g-FmWju_xs129PidYRSMyxhFww7XgQHflpI0K0FDVqZSTk_mWiTANnLy7fJydTP8UDziWyU7RYSShlGcsO0ws-NGcikEk1d_7hA56CNhgaM; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A1%7D%22; IsDouyinActive=true',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.douyin.com/?recommend=1',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'uifid': '63bdc4b4b456901f349a081bfd3a24da10a1c6623f0a2d5eadd83f51c9f4d1123e3e881c56f5c5c435ebd0a12a8a9b7056ae64added34f6177501a2c86a624823ee63c1e1189427b288602a280743f12777b39b10b7e07b5704d3065525da753e2eac54a5d7aa41e04f96816347e74e8fe0430e9a92c601f70ab1e81413739ddc2ebe139901f83a48139c9f34001c042785d0d16e68aada1d0b2c3e0d8b16830',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    # 年月日
    now = datetime.datetime.now()
    year = str(now.year)  # 年
    month = str(now.month)  # 月
    day = now.day

    local_img_path = f"douyin_cover_image/{year}/{month}/{day}"  # 存再本地的抖音封面图
    if not os.path.exists(local_img_path):
        os.makedirs(local_img_path)
        print(f"目录 '{local_img_path}' 已创建。")
    else:
        print(f"目录 '{local_img_path}' 已存在，跳过创建。")

    local_img = local_img_path +"/" + f"{aweme_id}.jpg"
    resp = requests.get(cover_url,headers=headers)
    #下载图片
    try:
        with open(local_img,mode="wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):  # 分块下载
                if chunk:  # 确保块不为空
                    f.write(chunk)
    except:
        print("下载失败")
        return None
    min_client = MinioClient()
    min_client.upload_file("dev", local_img, local_img)
    pass

def task():
    # url_dist = splpt_url(url)
    url_list = read_xlsx()[591:]
    for url in url_list:
        sec_user_id = extract_sec_uid(url)
        if sec_user_id == None:
            print(url, "不合适")
            continue
        # sec_user_id = url_dist['sec_user_id']
        # locate_item_id = url_dist['locate_item_id']
        print(sec_user_id, "开始")
        short_douyin_id = get_author_info_json(sec_user_id, url)
        if short_douyin_id == None:
            continue
        # print("睡个10-15s")
        # time.sleep(random.randint(10,15))
        get_video_json(sec_user_id, 0, short_douyin_id, url)
        print(sec_user_id, "完成，睡个30-65s")
        time.sleep(random.randint(30, 65))
    pass

def main():
    start_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    end_time = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)

    while datetime.now() < start_time:
        time.sleep(timedelta(minutes=30).total_seconds())  # 等到开始时间

    while datetime.now() < end_time:
        task_start = datetime.now()
        task_duration = timedelta(hours=2) + timedelta(minutes=random.randint(-20, 20))
        rest_duration = timedelta(minutes=30) + timedelta(minutes=random.randint(-10, 10))

        while datetime.now() - task_start < task_duration:
            task()  # 执行任务

        print(f"Resting for {rest_duration.total_seconds() / 60:.1f} minutes...")
        time.sleep(rest_duration.total_seconds())
    pass

def delete_temp_files(files):
    """
    删除传入的文件列表中的所有临时文件。

    :param files: 文件路径的列表
    """
    for file in files:
        try:
            if os.path.exists(file):
                os.remove(file)
                print(f"已删除临时文件: {file}")
            else:
                print(f"文件不存在: {file}")
        except Exception as e:
            print(f"删除文件 {file} 时出错: {e}")

#下载视频的
def download_video(url,output_path):
    print("开始下载视频：", url)
    try:
        # 启用流式下载
        with requests.get(url,headers=get_header(), stream=True) as resp:
            resp.raise_for_status()  # 检查请求是否成功
            # 确保文件路径正确
            with open(output_path, mode="wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):  # 分块下载
                    if chunk:  # 确保块不为空
                        f.write(chunk)
        print(f"视频已成功下载到 {output_path}")
    except requests.exceptions.RequestException as e:
        print(f"下载失败：{e}")


if __name__ == '__main__':
    # task()
    # print("所有数据爬取完成")
    cover_url = "https://p9-pc-sign.douyinpic.com/obj/tos-cn-i-dy/62342c2b3609469caf4483740652cbdf?lk3s=138a59ce&x-expires=2051661600&x-signature=Que71sM0JpoloWLzC08BNWSIZQQ%3D&from=327834062&s=PackSourceEnum_PUBLISH&se=false&sc=cover&biz_tag=pcweb_cover&l=202501081011463957D7C67D514A46E5DC"
    aw_id = "2051661600"
    # set_into_minio(cover_url,aw_id)
    "https://www.douyin.com/aweme/v1/play/?video_id=v0d00fg10000ct6gjq7og65hb7epru10&line=0&file_id=0f929de96c6d46838f0444d84facd6ce&sign=4f2166a1204fb40048c38c6f7f4de86a&is_play_url=1&source=PackSourceEnum_PUBLISH"
    "https://www.douyin.com/aweme/v1/play/?video_id=v0200fg10000ctetgjvog65spuekh1c0&line=0&file_id=efea5a6201b04cf7b79f3d1f4addd66c&sign=26caee39cf3ec7b6367b0dd681d1f93e&is_play_url=1&source=PackSourceEnum_PUBLISH"
    "https://www.douyin.com/aweme/v1/play/?video_id=v0d00fg10000csih9f7og65i1lo1fa60&line=0&file_id=9dd8a7608bb241cf9d17ae0abd408068&sign=84566529ee120255ce8eea7813bc9f26&is_play_url=1&source=PackSourceEnum_PUBLISH"
    "https://www.douyin.com/user/MS4wLjABAAAAsZZCLqwXW95gYgQ-fIbYgo06K1WzoPUmiEbfS-DWe_ZDywD5OYQxCkcinmopaju8?from_tab_name=main&modal_id=7447101688634281251&vid=7444117774001065255"
    delete_temp_files(["douyin_cover_image/2025/1/8/2051661600.jpg"])

    pass







