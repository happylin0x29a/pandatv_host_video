#!/usr/bin/env python
# coding:utf-8
"""

@version:  3.4.4
@author:  linfeng
@file:  base_crawl.py
@time: 2019/3/16 16:45
"""
import os
import sys


class BaseCrawl(object):

    def __init__(self, host_id) -> None:
        self.headers = self.make_headers()
        self.download_path = self.__make_path(host_id)

    def make_headers(self):
        headers = dict()
        headers["Referer"] = "https://v.panda.tv/video/70450"
        headers[
            "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
        return headers

    @staticmethod
    def __make_path(host_id):
        project_path = os.path.dirname(sys.argv[0])
        download_path = os.path.join(project_path, "download")
        download_path = os.path.join(download_path, str(host_id))
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        return download_path
