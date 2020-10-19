#!/usr/bin/env python
# -- coding:utf-8 --

# pip install requests

import requests

r = requests.get('https://api.github.com/events')

# r is a response object <class 'requests.models.Response'>
# print(type(r))  

# other methods 
# r = requests.post('http://httpbin.org/post', data = {'key':'value'})
# r = requests.put('http://httpbin.org/put', data = {'key':'value'})
# r = requests.delete('http://httpbin.org/delete')
# r = requests.head('http://httpbin.org/get')
# r = requests.options('http://httpbin.org/get')

# construct URL
# payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
# r = requests.get('http://httpbin.org/get', params=payload)
# print(r.url)

# show the response data
# print(r.text)

# show the encoding and you can set encoding
# print(r.encoding)
# r.encoding='gbk'

# show the binary content
# print(r.content)

# status code  eg. 200
print(r.status_code)
