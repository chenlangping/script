#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import requests
import logging
import threadpool
import os
from bs4 import BeautifulSoup


class Setting(object):
    url = "https://k.sina.cn/article_7018619077_1a257a0c500100s4r6.html?from=cul"
    timeout = 7
    poolsize = 30


class NetworkException(Exception):
    # do something when network sucks!
    pass


class Cli(object):
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    }

    def __init__(self):
        super(Cli, self).__init__()
        self.s = requests.Session()
        self.s.headers = self.headers
        self.s.timeout = Setting.timeout
        self.logger = logging.getLogger('logger')

    def get(self, url, *args, **kwargs):
        r = self.s.get(url, *args, **kwargs)
        if r.status_code != requests.codes.ok:
            raise NetworkException
        return r

    def post(self, url, *args, **kwargs):
        r = self.s.post(url, *args, **kwargs)
        if r.status_code != requests.codes.ok:
            raise NetworkException
        return r


def init_logger():
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    logger_handler = logging.StreamHandler()
    logger_handler.setLevel(logging.DEBUG)
    logger_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))
    logger.addHandler(logger_handler)


def main():
    l = []
    mkdir(os.getcwd() + os.sep + "picture")
    init_logger()
    c = Cli()
    c.get(Setting.url)
    html_doc = c.get(Setting.url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    for link in soup.find_all("img"):
        if link.get("src").startswith("http"):
            l.append(link.get("src"))
    pool = threadpool.ThreadPool(Setting.poolsize)
    pool_requests = threadpool.makeRequests(download_picture, l)
    [pool.putRequest(req) for req in pool_requests]
    pool.wait()


def download_picture(picture_url):
    logger = logging.getLogger("logger")
    logger.info("start downloading picture from {}".format(picture_url))
    r = requests.get(picture_url, headers=Cli.headers)
    name = picture_url.split("/")[-1].split(".")[0]
    with open("./picture/" + name + ".jpg", "wb") as f:
        f.write(r.content)
    logger.info("picture {}.jpg has been downloaded".format(name))


def mkdir(path):
    folder = os.path.exists(path)
    logger = logging.getLogger("logger")
    if not folder:
        logger.info("creating new folder...")
        os.makedirs(path)
    else:
        logger.info("folder exists")


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    logging.getLogger("logger").info("done,time = {}".format(end - start))
