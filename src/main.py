#!/usr/bin/env python
# coding:utf-8
"""

@version:  3.4.4
@author:  linfeng
@file:  main.py
@time: 2019/3/16 15:33
"""
import time
from crawl import Crawl

MY_LOVE_ID = 119783794
ID_LIST = [119783794, 144742298, 147873818, 68898944, 30479320, 109403210, 97818468, 31426688, 49122768, 149419248,
           92370366, 136599150, 29806942]


def main():
    for id in ID_LIST:
        c = Crawl("https://vod.gate.panda.tv/api/hostvideos", id)
        c.start()
        time.sleep(30 * 60)


if __name__ == '__main__':
    main()
