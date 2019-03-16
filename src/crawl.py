#!/usr/bin/env python
# coding:utf-8
"""

@version:  3.4.4
@author:  linfeng
@file:  crawl.py
@time: 2019/3/16 15:43
"""
import requests
import time
from crawl_video import CrawlVideo
from base_crawl import BaseCrawl


class Crawl(BaseCrawl):

    def __init__(self, host_url: str, hostid: int) -> None:
        super().__init__(hostid)
        self.url = host_url
        self.host_id = hostid
        self.params = self.__make_params()

    def start(self):
        self.__get_m3u8_url()

    def __make_params(self):
        params = dict()
        params["pageno"] = 1
        params["pagenum"] = 20
        params["__plat"] = "pc_web"
        params["_"] = int(time.time() * 1000)
        params["hostid"] = self.host_id
        return params

    def __get_m3u8_url(self):
        page_no = 1
        length = 0
        while True:
            try:
                r = requests.get(self.url, headers=self.headers, params=self.params).json()
                video_list = r["data"]["items"]
                len_ = len(video_list)
                length += len_
                if len_ > 0:
                    for item in video_list:
                        c_process = CrawlVideo(item["v_url"], item["title"], self.host_id)
                        c_process.start()
                        c_process.join() #想求稳（慢一点） 就取消注释
                else:
                    print("获取m3u8 URL完毕,视频总数:", length)
                    break
            except BaseException as exception:
                print("获取m3u8 url异常%s" % exception)
            page_no += 1
            self.params["pageno"] = page_no


if __name__ == "__main__":
    c = Crawl("https://vod.gate.panda.tv/api/hostvideos", 119783794)
    c.start()
