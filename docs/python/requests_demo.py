#!/usr/bin/env python
# -- coding:utf-8 --
import requests


class URL(object):
    url = "www.example.com"


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


def main():
    c = Cli()
    c.get(URL.url)


if __name__ == '__main__':
    main()
