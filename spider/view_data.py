# coding:utf-8

import json
import re
from multiprocessing.dummy import Pool

import requests
from django.core.cache import cache
from django.http import JsonResponse

from spider.models import BvInfo

baseUrl = "https://www.bilibili.com/video/BV"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 "
                  "Safari/537.36 "
}
jQuery = "jQuery331030945337454615673"
CACHE_TIME_OUT = 30


def get_bv(bv_name):
    if len(bv_name) < 5:
        raise Exception("bv长度过短")
    if bv_name[:2].upper() == "BV":
        bv_name = bv_name[2:]
    url = "{0}{1}".format(baseUrl, bv_name)
    print(url)
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception("请求失败，请求码为{}".format(response.status_code))
    try:
        data = re.findall(r"<script>window\.__INITIAL_STATE__.*?;\(function", response.text, flags=re.S)
        data = json.loads(data[0][33:-10], strict=False)
        return data
    except Exception as e:
        raise Exception("解析出错，错误原因：{}".format(str(e)))


def save_bv(bv_name):
    if bv_name[:2].upper() == "BV":
        bv = "BV" + bv_name[2:]
    bv = BvInfo.objects.get(bvid=bv_name)
    if not bv:
        bv = BvInfo()
    data = get_bv(bv.bvid)
    bv.avid = data["videoData"]["aid"]
    bv.bvid = data["videoData"]["bvid"]
    bv.desc = data["videoData"]["desc"]
    bv.title = data["videoData"]["title"]
    bv.pages = len(data["videoData"]["pages"])
    bv.ctime = data["videoData"]["ctime"]
    bv.pubdate = data["videoData"]["pubdate"]
    bv.duration = data["videoData"]["duration"]
    bv.stat_view = data["videoData"]["stat"]["view"]
    bv.stat_danmaku = data["videoData"]["stat"]["danmaku"]
    bv.stat_reply = data["videoData"]["stat"]["reply"]
    bv.stat_favorite = data["videoData"]["stat"]["favorite"]
    bv.stat_coin = data["videoData"]["stat"]["coin"]
    bv.stat_share = data["videoData"]["stat"]["share"]
    bv.stat_like = data["videoData"]["stat"]["like"]
    bv.own_mid = data["upData"]["mid"]
    bv.own_name = data["upData"]["name"]
    bv.save()
    cache.set(bv.bvid, {"code": 0,})
    return {'success': True, 'msg': bv.title, 'bv': bv.bvid}


def get_bv_cache_callback(args):
    bv = args["bv"]
    cache.set(bv, {"code": 0, "msg": args["msg"]}, timeout=CACHE_TIME_OUT)


def get_bv_cache(bv_name):
    cache.set(bv_name, {"code": 1, "msg": "正在加载"}, timeout=CACHE_TIME_OUT)
    try:
        pool = Pool(processes=1)
        pool.apply_async(save_bv, args=(bv_name,), callback=get_bv_cache_callback)
        pool.close()
    except Exception as e:
        cache.set(bv_name, {"code": 2, "msg": "出错:{}".format(str(e))}, timeout=CACHE_TIME_OUT)


def save_bv_sync(bv_name):
    data = cache.get(bv_name)
    if data:
        return {'success': True, 'msg': data.get('msg')}
    get_bv_cache(bv_name)
    return {'success': True, 'msg': '正在加载'}


if __name__ == '__main__':
    get_bv("BV1d44y1H7gP")
