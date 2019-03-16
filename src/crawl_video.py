#!/usr/bin/env python
# coding:utf-8
"""

@version:  3.4.4
@author:  linfeng
@file:  crawl_video.py
@time: 2019/3/16 16:04
"""
import os
import re
import requests
from multiprocessing import Process
from urllib.parse import urlparse
from base_crawl import BaseCrawl


class CrawlVideo(Process, BaseCrawl):
    def __init__(self, m3u8_url: str, title: str, id: int) -> None:
        """
        :param m3u8_url: https://pl-vod28.live.panda.tv/transcode/1764801/2019-03-01/cf72fe2cb073746bc325f538a474ea93/index.m3u8
        :param title:
        """
        Process.__init__(self)
        BaseCrawl.__init__(self, id)
        self.url = m3u8_url
        self.path_url = self.__get_path_url()
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        title = re.sub(rstr, "", title)
        self.title = "".join(title.split()).replace("！", "").replace("？", "") + ".mp4"

    def run(self):
        print("开始爬取:", self.title)
        m3u8_content = requests.get(self.url, headers=self.headers).text
        self.__parse_m3u8(m3u8_content)

    def __parse_m3u8(self, m3u8_content: str):
        if "#EXTM3U" not in m3u8_content:
            print("m3u8 内容有误")
            return
        content_list = m3u8_content.split("\n")
        for index, item in enumerate(content_list):
            if "#EXTINF" in item:
                url = self.__get_ts_url(content_list[index + 1])
                self.__loop_try(url)
        print("爬取%s 完毕" % self.title)

    def __loop_try(self, url):
        while True:
            try:
                response = requests.get(url, headers=self.headers, stream=True, timeout=60)
                file_path = os.path.join(self.download_path, self.title)
                with open(file_path, "ab") as data:
                    for chunk in response.iter_content(chunk_size=102400):
                        if chunk:
                            data.write(chunk)
                            data.flush()
                break
            except BaseException as exception:
                print("爬取:%s 出错:%s,重试中" % (url, exception))

    def __get_path_url(self):
        url_parse = urlparse(self.url)
        path_list = url_parse.path.strip().split("/")
        path = "https://" + url_parse.hostname + "/" + "/".join(path_list[1:-1])
        return path

    def __get_ts_url(self, ts_name: str):
        """

        :return:https://pl-vod28.live.panda.tv/transcode/1764801/2019-03-01/cf72fe2cb073746bc325f538a474ea93/index_0.ts
        """
        path = self.path_url + "/" + ts_name
        print("ts path:", path)
        return path
