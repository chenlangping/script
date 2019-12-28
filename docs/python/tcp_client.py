#!/usr/bin/env python
# -- coding:utf-8 --


import socket

target_ip = "127.0.0.1"
target_port = 38456

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_ip, target_port))
client.send(b"hello server")
print(client.recv(4096))
